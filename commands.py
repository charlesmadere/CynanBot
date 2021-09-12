import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from twitchio.ext.commands import Context

import CynanBotCommon.utils as utils
import twitchUtils
from cutenessRepository import CutenessRepository
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.languagesRepository import (LanguageEntry,
                                                LanguagesRepository)
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWarsQuotesRepository import StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timedDict import TimedDict
from CynanBotCommon.translationHelper import TranslationHelper
from CynanBotCommon.triviaGameRepository import (TriviaGameCheckResult,
                                                 TriviaGameRepository)
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.weatherRepository import WeatherRepository
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from doubleCutenessHelper import DoubleCutenessHelper
from generalSettingsRepository import GeneralSettingsRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx: Context):
        pass


class AnalogueCommand(AbsCommand):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        usersRepository: UsersRepository
    ):
        if analogueStoreRepository is None:
            raise ValueError(f'analogueStoreRepository argument is malformed: \"{analogueStoreRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__analogueStoreRepository: AnalogueStoreRepository = analogueStoreRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastAnalogueStockMessageTimes: TimedDict = TimedDict(timedelta(minutes = 2, seconds = 30))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isAnalogueEnabled():
            return
        elif not self.__lastAnalogueStockMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        includePrices = 'includePrices' in splits

        try:
            result = self.__analogueStoreRepository.fetchStoreStock()
            await twitchUtils.safeSend(ctx, result.toStr(includePrices = includePrices))
        except (RuntimeError, ValueError):
            print(f'Error fetching Analogue stock in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching Analogue stock')


class AnswerCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        doubleCutenessHelper: DoubleCutenessHelper,
        generalSettingsRepository: GeneralSettingsRepository,
        triviaGameRepository: TriviaGameRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif doubleCutenessHelper is None:
            raise ValueError(f'doubleCutenessHelper argument is malformed: \"{doubleCutenessHelper}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__doubleCutenessHelper: DoubleCutenessHelper = doubleCutenessHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__triviaGameRepository: TriviaGameRepository = triviaGameRepository
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTriviaGameEnabled():
            return
        elif self.__triviaGameRepository.isAnswered(user.getHandle()):
            return

        seconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay()
        if user.hasWaitForTriviaAnswerDelay():
            seconds = user.getWaitForTriviaAnswerDelay()

        if not self.__triviaGameRepository.isWithinAnswerWindow(seconds, user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ You must provide the exact answer with the !answer command.')
            return

        answer = ' '.join(splits[1:])
        userId = str(ctx.author.id)

        checkResult = self.__triviaGameRepository.checkAnswer(
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = userId
        )

        if checkResult is TriviaGameCheckResult.INVALID_USER:
            return
        elif checkResult is TriviaGameCheckResult.INCORRECT_ANSWER:
            answerStr = self.__triviaGameRepository.getTrivia(user.getHandle()).getAnswerReveal()
            await twitchUtils.safeSend(ctx, f'😿 Sorry {ctx.author.name}, that is not the right answer. The correct answer is: {answerStr}')
            return
        elif checkResult is not TriviaGameCheckResult.CORRECT_ANSWER:
            print(f'Encounted a strange TriviaGameCheckResult when checking the answer to a trivia question: \"{checkResult}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Sorry, a \"{checkResult}\" error occurred when checking your answer to the trivia question.')
            return

        cutenessPoints = self.__generalSettingsRepository.getTriviaGamePoints()

        if user.hasTriviaGamePoints():
            cutenessPoints = user.getTriviaGamePoints()

        if self.__doubleCutenessHelper.isWithinDoubleCuteness(user.getHandle()):
            cutenessPoints = 2 * cutenessPoints

        try:
            cutenessResult = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = cutenessPoints,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            await twitchUtils.safeSend(ctx, f'🎉 Congratulations {ctx.author.name}, you are correct! 🎉 Your cuteness is now {cutenessResult.getCutenessStr()}~ ✨')
        except ValueError:
            print(f'Error increasing cuteness for {ctx.author.name} ({userId}) in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error increasing cuteness for {ctx.author.name}')


class CommandsCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        commands = list()
        commands.append('!cynansource')

        if user.hasDiscord():
            commands.append('!discord')

        if user.hasSpeedrunProfile():
            commands.append('!pbs')

        if user.hasTimeZones():
            commands.append('!time')

        if user.hasTwitter():
            commands.append('!twitter')

        if user.isAnalogueEnabled():
            commands.append('!analogue')

        if user.isCutenessEnabled():
            commands.append('!cuteness')
            commands.append('!mycuteness')

            if user.isGiveCutenessEnabled() and ctx.author.is_mod:
                commands.append('!givecuteness')

        if user.isDiccionarioEnabled():
            commands.append('!diccionario')

        if user.isJishoEnabled():
            commands.append('!jisho')

        if user.isJokesEnabled():
            commands.append('!joke')

        if user.isPokepediaEnabled():
            commands.append('!pkmon')
            commands.append('!pkmove')

        if user.isStarWarsQuotesEnabled():
            commands.append('!swquote')

        if user.isTamalesEnabled():
            commands.append('!tamales')

        if user.isTranslateEnabled():
            commands.append('!translate')

        if user.isTriviaEnabled() and not user.isTriviaGameEnabled():
            commands.append('!trivia')

        if user.isWeatherEnabled():
            commands.append('!weather')

        if user.isWordOfTheDayEnabled():
            commands.append('!word')

        commands.sort()
        commandsString = ', '.join(commands)

        await twitchUtils.safeSend(ctx, f'My commands: {commandsString}')

class CutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastCutenessMessageTimes: TimedDict = TimedDict(timedelta(seconds = 10))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastCutenessMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        userName: str = None
        if len(splits) >= 2:
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.author.name

        userId: str = None

        # this means that a user is querying for another user's cuteness
        if userName.lower() != ctx.author.name.lower():
            try:
                userId = self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                print(f'Unable to find user ID for \"{userName}\" in the database (Twitch channel is \"{user.getHandle()}\")')
                await twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = self.__cutenessRepository.fetchCuteness(
                fetchLocalLeaderboard = True,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await twitchUtils.safeSend(ctx, result.toStr())
        else:
            userId = str(ctx.author.id)

            result = self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = user.getHandle(),
                specificLookupUserId = userId,
                specificLookupUserName = userName
            )

            await twitchUtils.safeSend(ctx, result.toStr())


class DiccionarioCommand(AbsCommand):

    def __init__(
        self,
        enEsDictionary: EnEsDictionary,
        usersRepository: UsersRepository
    ):
        if enEsDictionary is None:
            raise ValueError(f'enEsDictionary argument is malformed: \"{enEsDictionary}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__enEsDictionary: EnEsDictionary = enEsDictionary
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastDiccionarioMessageTimes: TimedDict = TimedDict(timedelta(seconds = 15))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isDiccionarioEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastDiccionarioMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ A search term is necessary for the !diccionario command. Example: !diccionario beer')
            return

        query = ' '.join(splits[1:])

        try:
            result = self.__enEsDictionary.search(query)
            self.__lastDiccionarioMessageTimes.update(user.getHandle())
            await twitchUtils.safeSend(ctx, result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error searching Spanish-English Dictionary for \"{query}\" in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error searching Spanish-English Dictionary for \"{query}\"')


class DiscordCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasDiscord():
            return

        discord = user.getDiscordUrl()
        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s discord: {discord}')


class GiveCutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        if not ctx.author.is_mod:
            return

        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled() or not user.isGiveCutenessEnabled():
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 3:
            await twitchUtils.safeSend(ctx, f'⚠ Username and amount is necessary for the !givecuteness command. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = splits[1]
        if not utils.isValidStr(userName):
            print(f'Username is malformed: \"{userName}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            print(f'Increment amount is malformed: \"{incrementAmountStr}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, ValueError):
            print(f'Unable to convert increment amount into an int: \"{incrementAmountStr}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = utils.removePreceedingAt(userName)

        try:
            userId = self.__userIdsRepository.fetchUserId(userName = userName)
        except ValueError:
            print(f'Attempted to give cuteness to \"{userName}\", but their user ID does not exist in the database')
            await twitchUtils.safeSend(ctx, f'⚠ Unable to give cuteness to \"{userName}\", they don\'t currently exist in the database')
            return

        try:
            result = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await twitchUtils.safeSend(ctx, f'✨ Cuteness for {userName} is now {result.getCutenessStr()} ✨')
        except ValueError:
            print(f'Error incrementing cuteness by {incrementAmount} for {userName} ({userId}) in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error incrementing cuteness for {userName}')


class JishoCommand(AbsCommand):

    def __init__(
        self,
        jishoHelper: JishoHelper,
        usersRepository: UsersRepository
    ):
        if jishoHelper is None:
            raise ValueError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__jishoHelper: JishoHelper = jishoHelper
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastJishoMessageTimes: TimedDict = TimedDict(timedelta(seconds = 8))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJishoEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastJishoMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query = splits[1]
        self.__lastJishoMessageTimes.update(user.getHandle())

        try:
            result = self.__jishoHelper.search(query)

            for string in result.toStrList():
                await twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError):
            print(f'Error searching Jisho for \"{query}\" in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error searching Jisho for \"{query}\"')


class JokeCommand(AbsCommand):

    def __init__(
        self,
        jokesRepository: JokesRepository,
        usersRepository: UsersRepository
    ):
        if jokesRepository is None:
            raise ValueError(f'jokesRepository argument is malformed: \"{jokesRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__jokesRepository: JokesRepository = jokesRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastJokeMessageTimes: TimedDict = TimedDict(timedelta(minutes = 1))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJokesEnabled():
            return
        elif not self.__lastJokeMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            result = self.__jokesRepository.fetchJoke()
            await twitchUtils.safeSend(ctx, result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching joke of the day in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching joke of the day')


class MyCutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMyCutenessMessageTimes: TimedDict = TimedDict(timedelta(seconds = 10))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMyCutenessMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userId = str(ctx.author.id)

        try:
            result = self.__cutenessRepository.fetchCuteness(
                fetchLocalLeaderboard = True,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            await twitchUtils.safeSend(ctx, result.toStr())
        except ValueError:
            print(f'Error retrieving cuteness for {ctx.author.name} ({userId}) in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving cuteness for {ctx.author.name}')


class PbsCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasSpeedrunProfile():
            return

        speedrunProfile = user.getSpeedrunProfile()
        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s speedrun profile: {speedrunProfile}')


class PkMonCommand(AbsCommand):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepository,
        usersRepository: UsersRepository
    ):
        if pokepediaRepository is None:
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastPkMonMessageTimes: TimedDict = TimedDict(timedelta(seconds = 30))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastPkMonMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ A Pokémon name is necessary for the !pkmon command. Example: !pkmon charizard')
            return

        name = splits[1]

        try:
            mon = self.__pokepediaRepository.searchPokemon(name)

            for string in mon.toStrList():
                await twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError):
            print(f'Error retrieving Pokemon: \"{name}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon: \"{name}\"')


class PkMoveCommand(AbsCommand):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepository,
        usersRepository: UsersRepository
    ):
        if pokepediaRepository is None:
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastPkMoveMessageTimes: TimedDict = TimedDict(timedelta(seconds = 30))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastPkMoveMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ A move name is necessary for the !pkmove command. Example: !pkmove fire spin')
            return

        name = ' '.join(splits[1:])

        try:
            move = self.__pokepediaRepository.searchMoves(name)

            for string in move.toStrList():
                await twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError):
            print(f'Error retrieving Pokemon move: \"{name}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon move: \"{name}\"')


class RaceCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository
        self.__lastRaceMessageTimes: TimedDict = TimedDict(timedelta(minutes = 2))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isRaceEnabled() or not ctx.author.is_mod:
            return
        elif not self.__lastRaceMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await twitchUtils.safeSend(ctx, '!race')


class StubCommand(AbsCommand):

    def __init__(self):
        pass

    async def handleCommand(self, ctx: Context):
        pass


class SwQuoteCommand(AbsCommand):

    def __init__(
        self,
        starWarsQuotesRepository: StarWarsQuotesRepository,
        usersRepository: UsersRepository
    ):
        if starWarsQuotesRepository is None:
            raise ValueError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__starWarsQuotesRepository: StarWarsQuotesRepository = starWarsQuotesRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastStarWarsQuotesMessageTimes: TimedDict = TimedDict(timedelta(seconds = 30))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isStarWarsQuotesEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastStarWarsQuotesMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        randomSpaceEmoji = utils.getRandomSpaceEmoji()
        splits = utils.getCleanedSplits(ctx.message.content)

        if len(splits) < 2:
            swQuote = self.__starWarsQuotesRepository.fetchRandomQuote()
            await twitchUtils.safeSend(ctx, f'{swQuote} {randomSpaceEmoji}')
            return

        query = ' '.join(splits[1:])

        try:
            swQuote = self.__starWarsQuotesRepository.searchQuote(query)

            if utils.isValidStr(swQuote):
                await twitchUtils.safeSend(ctx, f'{swQuote} {randomSpaceEmoji}')
            else:
                await twitchUtils.safeSend(ctx, f'⚠ No Star Wars quote found for the given query: \"{query}\"')
        except ValueError:
            print(f'Error retrieving Star Wars quote with query: \"{query}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Star Wars quote with query: \"{query}\"')


class TamalesCommand(AbsCommand):

    def __init__(
        self,
        tamaleGuyRepository: TamaleGuyRepository,
        usersRepository: UsersRepository
    ):
        if tamaleGuyRepository is None:
            raise ValueError(f'tamaleGuyRepository argument is malformed: \"{tamaleGuyRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__tamaleGuyRepository: TamaleGuyRepository = tamaleGuyRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastTamalesMessageTimes: TimedDict = TimedDict(timedelta(minutes = 5))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTamalesEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastTamalesMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            storeStock = self.__tamaleGuyRepository.fetchStoreStock()
            await twitchUtils.safeSend(ctx, storeStock.toStr())
        except (RuntimeError, ValueError):
            print('Error retrieving Tamale Guy store stock')
            await twitchUtils.safeSend(ctx, '⚠ Error retrieving Tamale Guy store stock')


class TimeCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTimeZones():
            return

        timeZones = user.getTimeZones()
        first = True
        text = ''

        for timeZone in timeZones:
            localTime = datetime.now(timeZone)

            if first:
                first = False
                formattedTime = utils.formatTime(localTime)
                text = f'🕰️ The local time for {user.getHandle()} is {formattedTime}.'
            else:
                formattedTime = utils.formatTimeShort(localTime)
                timeZoneName = timeZone.tzname(datetime.utcnow())
                text = f'{text} {timeZoneName} time is {formattedTime}.'

        await twitchUtils.safeSend(ctx, text)


class TranslateCommand(AbsCommand):

    def __init__(
        self,
        languagesRepository: LanguagesRepository,
        translationHelper: TranslationHelper,
        usersRepository: UsersRepository
    ):
        if languagesRepository is None:
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif translationHelper is None:
            raise ValueError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__translationHelper: TranslationHelper = translationHelper
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastTranslateMessageTimes: TimedDict = TimedDict(timedelta(seconds = 15))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTranslateEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastTranslateMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, f'⚠ Please specify the text you want to translate. Example: !translate I like tamales')
            return

        startSplitIndex = 1
        targetLanguageEntry: LanguageEntry = None
        if len(splits[1]) >= 3 and splits[1][0:2] == '--':
            targetLanguageEntry = self.__languagesRepository.getLanguageForCommand(
                command = splits[1][2:],
                hasIso6391Code = True
            )

            if targetLanguageEntry is not None:
                startSplitIndex = 2

        text = ' '.join(splits[startSplitIndex:])

        try:
            response = self.__translationHelper.translate(text, targetLanguageEntry)
            await twitchUtils.safeSend(ctx, response.toStr())
        except (RuntimeError, ValueError):
            print(f'Error translating text: \"{text}\"')
            await twitchUtils.safeSend(ctx, '⚠ Error translating')


class TriviaCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        triviaRepository: TriviaRepository,
        usersRepository: UsersRepository
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif triviaRepository is None:
            raise ValueError(f'triviaRepository argument is malformed: \"{triviaRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__triviaRepository: TriviaRepository = triviaRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastTriviaMessageTimes: TimedDict = TimedDict(timedelta(minutes = 5))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTriviaEnabled():
            return
        elif user.isTriviaGameEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastTriviaMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            response = self.__triviaRepository.fetchTrivia()
            await twitchUtils.safeSend(ctx, response.getPrompt())

            asyncio.create_task(twitchUtils.waitThenSend(
                messageable = ctx,
                delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay(),
                message = f'🥁 And the answer is: {response.getAnswerReveal()}'
            ))
        except (RuntimeError, ValueError) as e:
            print(f'Error retrieving trivia: {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error retrieving trivia')


class TwitterCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTwitter():
            return

        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s twitter: {user.getTwitterUrl()}')


class WeatherCommand(AbsCommand):
    
    def __init__(
        self,
        locationsRepository: LocationsRepository,
        usersRepository: UsersRepository,
        weatherRepository: WeatherRepository
    ):
        if locationsRepository is None:
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif weatherRepository is None:
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')

        self.__locationsRepository: LocationsRepository = locationsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__weatherRepository: WeatherRepository = weatherRepository
        self.__lastWeatherMessageTimes: TimedDict = TimedDict(timedelta(minutes = 2))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isWeatherEnabled():
            return
        elif not self.__lastWeatherMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        if not user.hasLocationId():
            await twitchUtils.safeSend(ctx, f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = self.__locationsRepository.getLocation(user.getLocationId())

        try:
            weatherReport = self.__weatherRepository.fetchWeather(location)
            await twitchUtils.safeSend(ctx, weatherReport.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching weather for \"{user.getLocationId()}\" in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching weather')


class WordCommand(AbsCommand):

    def __init__(
        self,
        languagesRepository: LanguagesRepository,
        usersRepository: UsersRepository,
        wordOfTheDayRepository: WordOfTheDayRepository
    ):
        if languagesRepository is None:
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif wordOfTheDayRepository is None:
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__wordOfTheDayRepository: WordOfTheDayRepository = wordOfTheDayRepository
        self.__lastWotdMessageTimes: TimedDict = TimedDict(timedelta(seconds = 8))

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isWordOfTheDayEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastWotdMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        if len(splits) < 2:
            exampleEntry = self.__languagesRepository.getExampleLanguageEntry(hasWotdApiCode = True)
            allWotdApiCodes = self.__languagesRepository.getAllWotdApiCodes()
            await twitchUtils.safeSend(ctx, f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.getWotdApiCode()}. Available languages: {allWotdApiCodes}')
            return

        language = splits[1]
        languageEntry = None

        try:
            languageEntry = self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except (RuntimeError, ValueError):
            print(f'Error retrieving language entry for \"{language}\" in {user.getHandle()}')
            allWotdApiCodes = self.__languagesRepository.getAllWotdApiCodes()
            await twitchUtils.safeSend(ctx, f'⚠ The given language code is not supported by the !word command. Available languages: {allWotdApiCodes}')
            return

        try:
            wotd = self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await twitchUtils.safeSend(ctx, wotd.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching word of the day for \"{languageEntry.getWotdApiCode()}\" in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error fetching word of the day for \"{languageEntry.getWotdApiCode()}\"')
