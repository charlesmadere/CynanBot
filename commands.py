import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import List

from twitchio.ext.commands import Context

import CynanBotCommon.utils as utils
import twitchUtils
from cuteness.cutenessRepository import CutenessRepository
from cuteness.doubleCutenessHelper import DoubleCutenessHelper
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languageEntry import LanguageEntry
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timedDict import TimedDict
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.triviaGameCheckResult import TriviaGameCheckResult
from CynanBotCommon.trivia.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaScoreResult import TriviaScoreResult
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from generalSettingsRepository import GeneralSettingsRepository
from triviaUtils import TriviaUtils
from users.userIdsRepository import UserIdsRepository
from users.usersRepository import UsersRepository


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx: Context):
        pass


class AnalogueCommand(AbsCommand):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if analogueStoreRepository is None:
            raise ValueError(f'analogueStoreRepository argument is malformed: \"{analogueStoreRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__analogueStoreRepository: AnalogueStoreRepository = analogueStoreRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isAnalogueEnabled():
            return
        elif not user.isAnalogueEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        includePrices = 'includePrices' in splits

        try:
            result = self.__analogueStoreRepository.fetchStoreStock()
            await twitchUtils.safeSend(ctx, result.toStr(includePrices = includePrices))
        except (RuntimeError, ValueError) as e:
            self.__timber.log('AnalogueCommand', f'Error fetching Analogue store stock: {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching Analogue store stock')

        self.__timber.log('AnalogueCommand', f'Handled !analogue command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class AnswerCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        doubleCutenessHelper: DoubleCutenessHelper,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameRepository: TriviaGameRepository,
        triviaScoreRepository: TriviaScoreRepository,
        triviaUtils: TriviaUtils,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif doubleCutenessHelper is None:
            raise ValueError(f'doubleCutenessHelper argument is malformed: \"{doubleCutenessHelper}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameRepository is None:
            raise ValueError(f'triviaGameRepository argument is malformed: \"{triviaGameRepository}\"')
        elif triviaScoreRepository is None:
            raise ValueError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif triviaUtils is None:
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__doubleCutenessHelper: DoubleCutenessHelper = doubleCutenessHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameRepository: TriviaGameRepository = triviaGameRepository
        self.__triviaScoreRepository: TriviaScoreRepository = triviaScoreRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled():
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
            self.__timber.log('AnswerCommand', f'{ctx.author.name}:{userId} in {user.getHandle()} answered incorrectly')
            answerStr = self.__triviaUtils.getAnswerReveal(self.__triviaGameRepository.getTrivia(user.getHandle()))
            await twitchUtils.safeSend(ctx, f'😿 Sorry {ctx.author.name}, that is not the right answer. {answerStr}')
            self.__triviaScoreRepository.incrementTotalLosses(user.getHandle(), userId)
            return
        elif checkResult is not TriviaGameCheckResult.CORRECT_ANSWER:
            self.__timber.log('AnswerCommand', f'Encounted a strange TriviaGameCheckResult when checking the answer to a trivia question: \"{checkResult}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Sorry, a \"{checkResult}\" error occurred when checking your answer to the trivia question.')
            return

        self.__triviaScoreRepository.incrementTotalWins(user.getHandle(), userId)

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

            self.__timber.log('AnswerCommand', f'Increased cuteness for {ctx.author.name}:{userId} by {cutenessPoints} in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'Congratulations {ctx.author.name}, you are correct! 🎉 Your cuteness is now {cutenessResult.getCutenessStr()}~ ✨')
        except ValueError:
            self.__timber.log('AnswerCommand', f'Error increasing cuteness for {ctx.author.name}:{userId} in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Error increasing cuteness for {ctx.author.name}')

        self.__timber.log('AnswerCommand', f'Handled !answer command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class ChatBandClearCommand(AbsCommand):

    def __init__(
        self,
        chatBandManager: ChatBandManager,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        usersRepository: UsersRepository
    ):
        if chatBandManager is None:
            raise ValueError(f'chatBandManager argument is malformed: \"{chatBandManager}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatBandManager: ChatBandManager = chatBandManager
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isChatBandEnabled():
            return
        elif not user.isChatBandEnabled():
            return
        elif not ctx.author.is_mod:
            return

        self.__chatBandManager.clearCaches()
        await twitchUtils.safeSend(ctx, 'ⓘ Chat Band caches cleared')
        self.__timber.log('ChatBandClearCommand', f'Handled !clearchatband command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class CommandsCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        commands: List[str] = list()

        if user.hasDiscord():
            commands.append('!discord')

        if user.hasSpeedrunProfile():
            commands.append('!pbs')

        if user.hasTimeZones():
            commands.append('!time')

        if user.hasTwitter():
            commands.append('!twitter')

        if self.__generalSettingsRepository.isAnalogueEnabled() and user.isAnalogueEnabled():
            commands.append('!analogue')

        if self.__generalSettingsRepository.isChatBandEnabled() and user.isChatBandEnabled() and ctx.author.is_mod:
            commands.append('!clearchatband')

        if user.isCutenessEnabled():
            commands.append('!cuteness')
            commands.append('!mycuteness')

            if user.isGiveCutenessEnabled() and ctx.author.is_mod:
                commands.append('!givecuteness')

        if user.isCynanSourceEnabled():
            commands.append('!cynansource')

        if self.__generalSettingsRepository.isJishoEnabled() and user.isJishoEnabled():
            commands.append('!jisho')

        if user.isJokesEnabled():
            commands.append('!joke')

        if self.__generalSettingsRepository.isPokepediaEnabled() and user.isPokepediaEnabled():
            commands.append('!pkmon')
            commands.append('!pkmove')

        if user.isStarWarsQuotesEnabled():
            commands.append('!swquote')

        if self.__generalSettingsRepository.isTamalesEnabled() and user.isTamalesEnabled():
            commands.append('!tamales')

        if self.__generalSettingsRepository.isTranslateEnabled() and user.isTranslateEnabled():
            commands.append('!translate')

        if self.__generalSettingsRepository.isTriviaEnabled() and user.isTriviaEnabled():
            commands.append('!trivia')

        if self.__generalSettingsRepository.isTriviaGameEnabled() and user.isTriviaGameEnabled():
            commands.append('!triviascore')

        if self.__generalSettingsRepository.isWeatherEnabled() and user.isWeatherEnabled():
            commands.append('!weather')

        if self.__generalSettingsRepository.isWordOfTheDayEnabled() and user.isWordOfTheDayEnabled():
            commands.append('!word')

        if not utils.hasItems(commands):
            return

        commands.sort()
        commandsString = self.__delimiter.join(commands)
        await twitchUtils.safeSend(ctx, f'ⓘ Available commands: {commandsString}')
        self.__timber.log('CommandsCommand', f'Handled !commands command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class CutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__timber: Timber = timber
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
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
                self.__timber.log('CutenessCommand', f'Unable to find user ID for \"{userName}\" in the database')
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

        self.__timber.log('CutenessCommand', f'Handled !cuteness command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class CynanSourceCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCynanSourceEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(ctx.channel.name):
            return

        await twitchUtils.safeSend(ctx, 'My source code is available here: https://github.com/charlesmadere/cynanbot')
        self.__timber.log('CynanSourceCommand', f'Handled !cynansource command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class DiscordCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasDiscord():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        discord = user.getDiscordUrl()
        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s discord: {discord}')


class GiveCutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__timber: Timber = timber
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
            self.__timber.log('GiveCutenessCommand', f'Username is malformed: \"{userName}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            self.__timber.log('GiveCutenessCommand', f'Increment amount is malformed: \"{incrementAmountStr}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Unable to convert increment amount into an int: \"{incrementAmountStr}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = utils.removePreceedingAt(userName)

        try:
            userId = self.__userIdsRepository.fetchUserId(userName = userName)
        except ValueError:
            self.__timber.log('GiveCutenessCommand', f'Unable to give cuteness to \"{userName}\", they don\'t current exist in the database')
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
        except ValueError as e:
            self.__timber.log('GiveCutenessCommand', f'Error giving {incrementAmount} cuteness to {userName}:{userId} in {user.getHandle()}: {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error giving cuteness to \"{userName}\"')

        self.__timber.log('GiveCutenessCommand', f'Handled !givecuteness command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class JishoCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: JishoHelper,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 8)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif jishoHelper is None:
            raise ValueError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__jishoHelper: JishoHelper = jishoHelper
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isJishoEnabled():
            return
        elif not user.isJishoEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query = splits[1]
        self.__lastMessageTimes.update(user.getHandle())

        try:
            result = self.__jishoHelper.search(query)

            for string in result.toStrList():
                await twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError) as e:
            self.__timber.log('JishoCommand', f'Error searching Jisho for \"{query}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error searching Jisho for \"{query}\"')

        self.__timber.log('JishoCommand', f'Handled !jisho command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class LoremIpsumCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        usersRepository: UsersRepository
    ):
        if timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isLoremIpsumEnabled():
            return
        elif not ctx.author.is_mod or not ctx.author.name.lower() == user.getHandle().lower():
            return

        loremIpsumText = ''
        if utils.randomBool():
            loremIpsumText = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eu scelerisque felis imperdiet proin. Id donec ultrices tincidunt arcu non sodales neque sodales. Amet consectetur adipiscing elit ut aliquam. Mattis pellentesque id nibh tortor id. Suspendisse interdum consectetur libero id faucibus nisl tincidunt. Amet cursus sit amet dictum sit amet justo. Sem integer vitae justo eget magna fermentum iaculis eu non. Augue ut lectus arcu bibendum at varius vel. Risus nullam eget felis eget nunc. Enim eu turpis egestas pretium aenean pharetra magna.'
        else:
            loremIpsumText = 'Bacon ipsum dolor amet t-bone sirloin tenderloin pork belly, shoulder landjaeger boudin. Leberkas short loin jowl short ribs, strip steak beef ribs flank pork belly ham corned beef. Spare ribs turkey sausage, tenderloin boudin brisket chislic shankle. Beef ribs ball tip ham hock beef t-bone porchetta bacon bresaola chislic swine. Pork meatball pancetta, jerky chuck burgdoggen tongue jowl fatback cupim doner rump flank landjaeger. Doner salami venison buffalo rump pork chop landjaeger jowl leberkas tail bresaola brisket spare ribs tri-tip sausage.'

        await twitchUtils.safeSend(ctx, loremIpsumText)
        self.__timber.log('LoremIpsumCommand', f'Handled !lorem command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class MyCutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
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
            self.__timber.log('MyCutenessCommand', f'Error retrieving cuteness for {ctx.author.name}:{userId}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving cuteness for {ctx.author.name}')

        self.__timber.log('MyCutenessCommand', f'Handled !mycuteness command for {ctx.author.name}:{userId} in {user.getHandle()}')


class PbsCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasSpeedrunProfile():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        speedrunProfile = user.getSpeedrunProfile()
        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s speedrun profile: {speedrunProfile}')


class PkMonCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        pokepediaRepository: PokepediaRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif pokepediaRepository is None:
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isPokepediaEnabled():
            return
        elif not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
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
        except (RuntimeError, ValueError) as e:
            self.__timber.log('PkMonCommand', f'Error retrieving Pokemon \"{name}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon \"{name}\"')


class PkMoveCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        pokepediaRepository: PokepediaRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif pokepediaRepository is None:
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isPokepediaEnabled():
            return
        elif not user.isPokepediaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
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
        except (RuntimeError, ValueError) as e:
            self.__timber.log('PkMoveCommand', f'Error retrieving Pokemon move: \"{name}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon move: \"{name}\"')


class RaceCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastRaceMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        if not ctx.author.is_mod:
            return

        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isRaceEnabled():
            return
        elif not self.__lastRaceMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await twitchUtils.safeSend(ctx, '!race')
        self.__timber.log('RaceCommand', f'Handled !race command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class StubCommand(AbsCommand):

    def __init__(self):
        pass

    async def handleCommand(self, ctx: Context):
        pass


class SwQuoteCommand(AbsCommand):

    def __init__(
        self,
        starWarsQuotesRepository: StarWarsQuotesRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if starWarsQuotesRepository is None:
            raise ValueError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__starWarsQuotesRepository: StarWarsQuotesRepository = starWarsQuotesRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isStarWarsQuotesEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
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
            self.__timber.log('SwQuoteCommand', f'Error retrieving Star Wars quote with query: \"{query}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Star Wars quote with query: \"{query}\"')


class TamalesCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        tamaleGuyRepository: TamaleGuyRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif tamaleGuyRepository is None:
            raise ValueError(f'tamaleGuyRepository argument is malformed: \"{tamaleGuyRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__tamaleGuyRepository: TamaleGuyRepository = tamaleGuyRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTamalesEnabled():
            return
        elif not user.isTamalesEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            storeStock = self.__tamaleGuyRepository.fetchStoreStock()
            await twitchUtils.safeSend(ctx, storeStock.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('TamalesCommand', f'Error retrieving Tamale Guy store stock: {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error retrieving Tamale Guy store stock')

        self.__timber.log('TamalesCommand', f'Handled !tamales command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class TimeCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTimeZones():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
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
        self.__timber.log('TimeCommand', f'Handled !time command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class TranslateCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        languagesRepository: LanguagesRepository,
        timber: Timber,
        translationHelper: TranslationHelper,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 15)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif languagesRepository is None:
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif translationHelper is None:
            raise ValueError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__timber: Timber = timber
        self.__translationHelper: TranslationHelper = translationHelper
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __determineOptionalLanguageEntry(self, splits: List[str]) -> LanguageEntry:
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

        if len(splits[1]) >= 3 and splits[1][0:2] == '--':
            return self.__languagesRepository.getLanguageForCommand(
                command = splits[1][2:],
                hasIso6391Code = True
            )

        return None

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTranslateEnabled():
            return
        elif not user.isTranslateEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, f'⚠ Please specify the text you want to translate. Example: !translate I like tamales')
            return

        targetLanguageEntry = self.__determineOptionalLanguageEntry(splits)

        startSplitIndex: int = 1
        if targetLanguageEntry is not None:
            startSplitIndex = 2

        text = ' '.join(splits[startSplitIndex:])

        try:
            response = self.__translationHelper.translate(text, targetLanguageEntry)
            await twitchUtils.safeSend(ctx, response.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('TranslateCommand', f'Error translating text: \"{text}\": {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error translating')

        self.__timber.log('TranslateCommand', f'Handled !translate command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class TriviaCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaRepository: TriviaRepository,
        triviaUtils: TriviaUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaRepository is None:
            raise ValueError(f'triviaRepository argument is malformed: \"{triviaRepository}\"')
        elif triviaUtils is None:
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaRepository: TriviaRepository = triviaRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTriviaEnabled():
            return
        elif not user.isTriviaEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        try:
            triviaQuestion = self.__triviaRepository.fetchTrivia(user.getHandle())
            await twitchUtils.safeSend(ctx, triviaQuestion.getPrompt())

            asyncio.create_task(twitchUtils.waitThenSend(
                messageable = ctx,
                delaySeconds = self.__generalSettingsRepository.getWaitForTriviaAnswerDelay(),
                message = f'🥁 {self.__triviaUtils.getAnswerReveal(triviaQuestion)}'
            ))
        except (RuntimeError, ValueError) as e:
            self.__timber.log('TriviaCommand', f'Error fetching trivia: {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching trivia')

        self.__timber.log('TriviaCommand', f'Handled !trivia command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class TriviaScoreCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaScoreRepository: TriviaScoreRepository,
        triviaUtils: TriviaUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaScoreRepository is None:
            raise ValueError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif triviaUtils is None:
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaScoreRepository: TriviaScoreRepository = triviaScoreRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        userName: str = None
        if len(splits) >= 2:
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.author.name

        userId: str = None

        # this means that a user is querying for another user's trivia score
        if userName.lower() != ctx.author.name.lower():
            try:
                userId = self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                self.__timber.log('TriviaScoreCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await twitchUtils.safeSend(ctx, f'⚠ Unable to find user ID for \"{userName}\" in the database')
                return
        else:
            userId = str(ctx.author.id)

        triviaResult = self.__triviaScoreRepository.fetchTriviaScore(
            twitchChannel = user.getHandle(),
            userId = userId
        )

        await twitchUtils.safeSend(ctx, self.__triviaUtils.getResults(userName, triviaResult))
        self.__timber.log('TriviaScoreCommand', f'Handled !triviascore command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class TwitterCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.hasTwitter():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s twitter: {user.getTwitterUrl()}')


class WeatherCommand(AbsCommand):
    
    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        locationsRepository: LocationsRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        weatherRepository: WeatherRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif locationsRepository is None:
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif weatherRepository is None:
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__locationsRepository: LocationsRepository = locationsRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__weatherRepository: WeatherRepository = weatherRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isWeatherEnabled():
            return
        elif not user.isWeatherEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        if not user.hasLocationId():
            await twitchUtils.safeSend(ctx, f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = self.__locationsRepository.getLocation(user.getLocationId())

        try:
            weatherReport = self.__weatherRepository.fetchWeather(location)
            await twitchUtils.safeSend(ctx, weatherReport.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WeatherCommand', f'Error fetching weather for \"{user.getLocationId()}\": {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching weather')

        self.__timber.log('WeatherCommand', f'Handled !weather command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class WordCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        languagesRepository: LanguagesRepository,
        timber: Timber,
        usersRepository: UsersRepository,
        wordOfTheDayRepository: WordOfTheDayRepository,
        cooldown: timedelta = timedelta(seconds = 10)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif languagesRepository is None:
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif wordOfTheDayRepository is None:
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__wordOfTheDayRepository: WordOfTheDayRepository = wordOfTheDayRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isWordOfTheDayEnabled():
            return
        elif not user.isWordOfTheDayEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)

        if len(splits) < 2:
            exampleEntry = self.__languagesRepository.getExampleLanguageEntry(hasWotdApiCode = True)
            allWotdApiCodes = self.__languagesRepository.getAllWotdApiCodes()
            await twitchUtils.safeSend(ctx, f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.getWotdApiCode()}. Available languages: {allWotdApiCodes}')
            return

        language = splits[1]
        languageEntry: LanguageEntry = None

        try:
            languageEntry = self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error retrieving language entry: \"{language}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ The given language code is not supported by the !word command. Available languages: {self.__languagesRepository.getAllWotdApiCodes()}')
            return

        try:
            wotd = self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await twitchUtils.safeSend(ctx, wotd.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\"')

        self.__timber.log('WordCommand', f'Handled !word command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')
