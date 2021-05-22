import asyncio
from abc import ABC, abstractmethod
from datetime import timedelta

import CynanBotCommon.utils as utils
from cutenessRepository import CutenessRepository
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWarsQuotesRepository import StarWarsQuotesRepository
from CynanBotCommon.timedDict import TimedDict
from CynanBotCommon.triviaGameRepository import (TriviaGameCheckResult,
                                                 TriviaGameRepository)
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.weatherRepository import WeatherRepository
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from generalSettingsRepository import GeneralSettingsRepository
from usersRepository import UsersRepository


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx):
        pass

    async def __sendDelayedMessage(self, messageable, delaySeconds: int, message: str):
        if messageable is None:
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidNum(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1:
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        await asyncio.sleep(delaySeconds)
        await messageable.send(message)


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

        self.__analogueStoreRepository = analogueStoreRepository
        self.__usersRepository = usersRepository
        self.__lastAnalogueStockMessageTimes = TimedDict(timedelta(minutes = 2, seconds = 30))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isAnalogueEnabled():
            return
        elif not self.__lastAnalogueStockMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        includePrices = 'includePrices' in splits

        try:
            result = self.__analogueStoreRepository.fetchStoreStock()
            await ctx.send(result.toStr(includePrices = includePrices))
        except (RuntimeError, ValueError):
            print(f'Error fetching Analogue stock in {user.getHandle()}')
            await ctx.send('⚠ Error fetching Analogue stock')


class AnswerCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        triviaGameRepository: TriviaGameRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository = cutenessRepository
        self.__generalSettingsRepository = generalSettingsRepository
        self.__triviaGameRepository = triviaGameRepository
        self.__usersRepository = usersRepository

    async def handleCommand(self, ctx):
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
            await ctx.send('⚠ You must provide the exact answer with the !answer command.')
            return

        answer = ' '.join(splits[1:])
        userId = str(ctx.author.id)

        checkResult = self.__triviaGameRepository.checkAnswer(
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = userId,
            userName = ctx.author.name
        )

        if checkResult is TriviaGameCheckResult.INVALID_USER:
            return
        elif checkResult is TriviaGameCheckResult.INCORRECT_ANSWER:
            answerStr = self.__triviaGameRepository.getTrivia(user.getHandle()).getCorrectAnswer()
            await ctx.send(f'😿 Sorry, that is not the right answer. The correct answer is: {answerStr}')
            return
        elif checkResult is not TriviaGameCheckResult.CORRECT_ANSWER:
            print(f'Encounted a strange TriviaGameCheckResult when checking the answer to a trivia question: \"{checkResult}\"')
            await ctx.send(f'⚠ Sorry, a \"{checkResult}\" error occurred when checking your answer to the trivia question.')
            return

        cutenessPoints = self.__generalSettingsRepository.getTriviaGamePoints()
        if user.hasTriviaGamePoints():
            cutenessPoints = user.getTriviaGamePoints()

        try:
            cutenessResult = self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = cutenessPoints,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            await ctx.send(f'🎉 Congratulations {ctx.author.name}! 🎉 You are correct! 🎉 Your new cuteness is now {cutenessResult.getCutenessStr()}~ ✨')
        except ValueError:
            print(f'Error increasing cuteness for {ctx.author.name} ({userId}) in {user.getHandle()}')
            await ctx.send(f'⚠ Error increasing cuteness for {ctx.author.name}')


class CutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository = cutenessRepository
        self.__usersRepository = usersRepository
        self.__lastCutenessMessageTimes = TimedDict(timedelta(seconds = 15))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastCutenessMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        userName = None
        if len(splits) >= 2:
            userName = splits[1]

        if utils.isValidStr(userName):
            userName = utils.removePreceedingAt(userName)

            try:
                result = self.__cutenessRepository.fetchCuteness(
                    twitchChannel = user.getHandle(),
                    userName = userName
                )

                if result.hasCuteness():
                    await ctx.send(f'✨ {userName}\'s cuteness: {result.getCutenessStr()} ✨')
                else:
                    await ctx.send(f'😿 Unfortunately {userName} has no cuteness 😿')
            except ValueError:
                print(f'Unable to find \"{userName}\" in the cuteness database')
                await ctx.send(f'⚠ Unable to find \"{userName}\" in the cuteness database')
        else:
            result = self.__cutenessRepository.fetchLeaderboard(user.getHandle())

            if result.hasEntries():
                await ctx.send(f'✨ Cuteness leaderboard — {result.toStr()} ✨')
            else:
                await ctx.send('😿 Unfortunately the cuteness leaderboard is empty 😿')


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

        self.__jishoHelper = jishoHelper
        self.__usersRepository = usersRepository
        self.__lastJishoMessageTimes = TimedDict(timedelta(seconds = 8))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJishoEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastJishoMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query = splits[1]
        self.__lastJishoMessageTimes.update(user.getHandle())

        try:
            result = self.__jishoHelper.search(query)
            await ctx.send(result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error searching Jisho for \"{query}\" in {user.getHandle()}')
            await ctx.send(f'⚠ Error searching Jisho for \"{query}\"')


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

        self.__jokesRepository = jokesRepository
        self.__usersRepository = usersRepository
        self.__lastJokeMessageTimes = TimedDict(timedelta(minutes = 1))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isJokesEnabled():
            return
        elif not self.__lastJokeMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            result = self.__jokesRepository.fetchJoke()
            await ctx.send(result.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching joke of the day in {user.getHandle()}')
            await ctx.send('⚠ Error fetching joke of the day')


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

        self.__pokepediaRepository = pokepediaRepository
        self.__usersRepository = usersRepository
        self.__lastPkMonMessageTimes = TimedDict(timedelta(seconds = 30))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastPkMonMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ A Pokémon name is necessary for the !pkmon command. Example: !pkmon charizard')
            return

        name = splits[1]

        try:
            mon = self.__pokepediaRepository.searchPokemon(name)
            strList = mon.toStrList()

            for s in strList:
                await ctx.send(s)
        except (RuntimeError, ValueError):
            print(f'Error retrieving Pokemon: \"{name}\"')
            await ctx.send(f'⚠ Error retrieving Pokémon: \"{name}\"')


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

        self.__pokepediaRepository = pokepediaRepository
        self.__usersRepository = usersRepository
        self.__lastPkMoveMessageTimes = TimedDict(timedelta(seconds = 30))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastPkMoveMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await ctx.send('⚠ A move name is necessary for the !pkmove command. Example: !pkmove fire spin')
            return

        name = ' '.join(splits[1:])

        try:
            move = self.__pokepediaRepository.searchMoves(name)
            strList = move.toStrList()

            for s in strList:
                await ctx.send(s)
        except (RuntimeError, ValueError):
            print(f'Error retrieving Pokemon move: \"{name}\"')
            await ctx.send(f'⚠ Error retrieving Pokémon move: \"{name}\"')


class RaceCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository = usersRepository
        self.__lastRaceMessageTimes = TimedDict(timedelta(minutes = 2))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isRaceEnabled() or not ctx.author.is_mod:
            return
        elif not self.__lastRaceMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await ctx.send('!race')


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

        self.__starWarsQuotesRepository = starWarsQuotesRepository
        self.__usersRepository = usersRepository
        self.__lastStarWarsQuotesMessageTimes = TimedDict(timedelta(seconds = 30))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isStarWarsQuotesEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastStarWarsQuotesMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        randomSpaceEmoji = utils.getRandomSpaceEmoji()
        splits = utils.getCleanedSplits(ctx.message.content)

        if len(splits) < 2:
            swQuote = self.__starWarsQuotesRepository.fetchRandomQuote()
            await ctx.send(f'{swQuote} {randomSpaceEmoji}')
            return

        query = ' '.join(splits[1:])

        try:
            swQuote = self.__starWarsQuotesRepository.searchQuote(query)

            if utils.isValidStr(swQuote):
                await ctx.send(f'{swQuote} {randomSpaceEmoji}')
            else:
                await ctx.send(f'⚠ No Star Wars quote found for the given query: \"{query}\"')
        except ValueError:
            print(f'Error retrieving Star Wars quote with query: \"{query}\"')
            await ctx.send(f'⚠ Error retrieving Star Wars quote with query: \"{query}\"')


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

        self.__generalSettingsRepository = generalSettingsRepository
        self.__triviaRepository = triviaRepository
        self.__usersRepository = usersRepository
        self.__lastTriviaMessageTimes = TimedDict(timedelta(minutes = 5))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isTriviaEnabled():
            return
        elif user.isTriviaGameEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastTriviaMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            response = self.__triviaRepository.fetchTrivia()
            await ctx.send(response.toPromptStr())

            asyncio.create_task(self.__sendDelayedMessage(
                messageable = ctx,
                delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay(),
                message = response.toAnswerStr()
            ))
        except (RuntimeError, ValueError):
            print(f'Error retrieving trivia')
            await ctx.send('⚠ Error retrieving trivia')


class TwitterCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository = usersRepository

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTwitter():
            return

        await ctx.send(f'{user.getHandle()}\'s twitter: {user.getTwitterUrl()}')


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

        self.__locationsRepository = locationsRepository
        self.__usersRepository = usersRepository
        self.__weatherRepository = weatherRepository
        self.__lastWeatherMessageTimes = TimedDict(timedelta(minutes = 2))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isWeatherEnabled():
            return
        elif not self.__lastWeatherMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        if not user.hasLocationId():
            await ctx.send(f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = self.__locationsRepository.getLocation(user.getLocationId())

        try:
            weatherReport = self.__weatherRepository.fetchWeather(location)
            await ctx.send(weatherReport.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching weather for \"{user.getLocationId()}\" in {user.getHandle()}')
            await ctx.send('⚠ Error fetching weather')


class WordCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository,
        wordOfTheDayRepository: WordOfTheDayRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif wordOfTheDayRepository is None:
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__usersRepository = usersRepository
        self.__wordOfTheDayRepository = wordOfTheDayRepository
        self.__lastWotdMessageTimes = TimedDict(timedelta(seconds = 8))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)
        
        if not user.isWordOfTheDayEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastWotdMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        languageList = self.__wordOfTheDayRepository.getLanguageList()

        if len(splits) < 2:
            example = languageList.getLanguages()[0].getPrimaryCommandName()
            languages = languageList.toCommandNamesStr()
            await ctx.send(f'⚠ A language code is necessary for the !word command. Example: !word {example}. Available languages: {languages}')
            return

        language = splits[1]
        languageEntry = None

        try:
            languageEntry = languageList.getLanguageForCommand(language)
        except (RuntimeError, ValueError):
            print(f'Error retrieving language entry for \"{language}\" in {user.getHandle()}')
            await ctx.send(f'⚠ The given language code is not supported by the !word command. Available languages: {languageList.toCommandNamesStr()}')
            return

        try:
            wotd = self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await ctx.send(wotd.toStr())
        except (RuntimeError, ValueError):
            print(f'Error fetching word of the day for \"{languageEntry.getApiName()}\" in {user.getHandle()}')
            await ctx.send(f'⚠ Error fetching word of the day for \"{languageEntry.getApiName()}\"')
