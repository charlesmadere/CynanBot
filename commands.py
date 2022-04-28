from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

from twitchio.ext.commands import Context

import CynanBotCommon.utils as utils
import twitch.twitchUtils as twitchUtils
from cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult
from cuteness.cutenessRepository import CutenessRepository
from cuteness.cutenessResult import CutenessResult
from cutenessUtils import CutenessUtils
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
from CynanBotCommon.trivia.checkAnswerTriviaAction import \
    CheckAnswerTriviaAction
from CynanBotCommon.trivia.checkSuperAnswerTriviaAction import \
    CheckSuperAnswerTriviaAction
from CynanBotCommon.trivia.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBotCommon.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
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
            result = await self.__analogueStoreRepository.fetchStoreStock()
            await twitchUtils.safeSend(ctx, result.toStr(includePrices = includePrices))
        except (RuntimeError, ValueError) as e:
            self.__timber.log('AnalogueCommand', f'Error fetching Analogue store stock: {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error fetching Analogue store stock')

        self.__timber.log('AnalogueCommand', f'Handled !analogue command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class AnswerCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        usersRepository: UsersRepository
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameMachine is None:
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled():
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ You must provide the exact answer with the !answer command.')
            return

        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckAnswerTriviaAction(
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = str(ctx.author.id),
            userName = ctx.author.name
        ))

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
            commands.append('!cutenesschampions')
            commands.append('!cutenesshistory')
            commands.append('!mycuteness')
            commands.append('!mycutenesshistory')

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
        cutenessUtils: CutenessUtils,
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif cutenessUtils is None:
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter

        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __cutenessLeaderboardResultToStr(self, result: CutenessLeaderboardResult) -> str:
        if result is None:
            raise ValueError(f'result argument is malformed: \"{result}\"')

        if not result.hasEntries():
            return f'Unfortunately the {result.getCutenessDate().toStr()} cuteness leaderboard is empty 😿'

        specificLookupText: str = None
        if result.hasSpecificLookupCutenessResult():
            userName = result.getSpecificLookupCutenessResult().getUserName()
            cutenessStr = result.getSpecificLookupCutenessResult().getCutenessStr()
            specificLookupText = f'{userName} your cuteness is {cutenessStr}'

        leaderboard = self.__cutenessUtils.getLeaderboard(result.getEntries(), self.__delimiter)

        if utils.isValidStr(specificLookupText):
            return f'{specificLookupText}, and the {result.getCutenessDate().toStr()} leaderboard is: {leaderboard} ✨'
        else:
            return f'The {result.getCutenessDate().toStr()} leaderboard is {leaderboard} ✨'

    def __cutenessResultToStr(self, result: CutenessResult) -> str:
        if result is None:
            raise ValueError(f'result argument is malformed: \"{result}\"')

        if result.hasCuteness() and result.getCuteness() >= 1:
            if result.hasLocalLeaderboard():
                localLeaderboard = self.__cutenessUtils.getLocalLeaderboard(result.getLocalLeaderboard(), self.__delimiter)
                return f'{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()}, and their local leaderboard is: {localLeaderboard} ✨'
            else:
                return f'{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'{result.getUserName()} has no cuteness in {result.getCutenessDate().toStr()}'

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
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                self.__timber.log('CutenessCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCuteness(
                fetchLocalLeaderboard = True,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await twitchUtils.safeSend(ctx, self.__cutenessResultToStr(result))
        else:
            userId = str(ctx.author.id)

            result = await self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = user.getHandle(),
                specificLookupUserId = userId,
                specificLookupUserName = userName
            )

            await twitchUtils.safeSend(ctx, self.__cutenessLeaderboardResultToStr(result))

        self.__timber.log('CutenessCommand', f'Handled !cuteness command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class CutenessChampionsCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif cutenessUtils is None:
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter

        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        result = await self.__cutenessRepository.fetchCutenessChampions(
            twitchChannel = user.getHandle()
        )

        await twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessChampions(result, self.__delimiter))
        self.__timber.log('CutenessChampionsCommand', f'Handled !cutenesschampions command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')

class CutenessHistoryCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' ✨ ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif cutenessUtils is None:
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif entryDelimiter is None:
            raise ValueError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif leaderboardDelimiter is None:
            raise ValueError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__entryDelimiter: str = entryDelimiter
        self.__leaderboardDelimiter: str = leaderboardDelimiter

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

        # this means that a user is querying for another user's cuteness history
        if userName.lower() != ctx.author.name.lower():
            try:
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                self.__timber.log('CutenessHistoryCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCutenessHistory(
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessHistory(result, self.__entryDelimiter))
        else:
            result = await self.__cutenessRepository.fetchCutenessLeaderboardHistory(
                twitchChannel = user.getHandle()
            )

            await twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessLeaderboardHistory(
                result = result,
                entryDelimiter = self.__entryDelimiter,
                leaderboardDelimiter = self.__leaderboardDelimiter
            ))

        self.__timber.log('CutenessHistoryCommand', f'Handled !cutenesshistory command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
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

        if not user.hasDiscord():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        discord = user.getDiscordUrl()
        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s discord: {discord}')
        self.__timber.log('DiscordCommand', f'Handled !discord command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
            self.__timber.log('GiveCutenessCommand', f'Less than 3 arguments given by {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')
            await twitchUtils.safeSend(ctx, f'⚠ Username and amount is necessary for the !givecuteness command. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = splits[1]
        if not utils.isValidStr(userName):
            self.__timber.log('GiveCutenessCommand', f'Username given by {ctx.author.name}:{ctx.author.id} in {user.getHandle()} is malformed: \"{userName}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            self.__timber.log('GiveCutenessCommand', f'Increment amount given by {ctx.author.name}:{ctx.author.id} in {user.getHandle()} is malformed: \"{incrementAmountStr}\"')
            await twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, TypeError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Unable to convert increment amount given by {ctx.author.name}:{ctx.author.id} in {user.getHandle()} into an int: \"{incrementAmountStr}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = utils.removePreceedingAt(userName)

        try:
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)
        except ValueError:
            self.__timber.log('GiveCutenessCommand', f'Unable to give {incrementAmount} cuteness from {ctx.author.name}:{ctx.author.id} in {user.getHandle()} to \"{userName}\", they don\'t current exist in the database')
            await twitchUtils.safeSend(ctx, f'⚠ Unable to give cuteness to \"{userName}\", they don\'t currently exist in the database')
            return

        try:
            result = await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await twitchUtils.safeSend(ctx, f'✨ Cuteness for {userName} is now {result.getCutenessStr()} ✨')
        except (OverflowError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Error giving {incrementAmount} cuteness from {ctx.author.name}:{ctx.author.id} in {user.getHandle()} to {userName}:{userId} in {user.getHandle()}: {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error giving cuteness to \"{userName}\"')

        self.__timber.log('GiveCutenessCommand', f'Handled !givecuteness command of {incrementAmount} for {userName}:{userId} from {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
            result = await self.__jishoHelper.search(query)

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
        cutenessUtils: CutenessUtils,
        timber: Timber,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if cutenessUtils is None:
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isCutenessEnabled():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userId = str(ctx.author.id)

        try:
            result = await self.__cutenessRepository.fetchCuteness(
                fetchLocalLeaderboard = True,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = ctx.author.name
            )

            await twitchUtils.safeSend(ctx, self.__cutenessUtils.getCuteness(result, self.__delimiter))
        except ValueError:
            self.__timber.log('MyCutenessCommand', f'Error retrieving cuteness for {ctx.author.name}:{userId}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving cuteness for {ctx.author.name}')

        self.__timber.log('MyCutenessCommand', f'Handled !mycuteness command for {ctx.author.name}:{userId} in {user.getHandle()}')


class MyCutenessHistoryCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if cutenessRepository is None:
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif cutenessUtils is None:
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter

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

        # this means that a user is querying for another user's cuteness history
        if userName.lower() != ctx.author.name.lower():
            try:
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                self.__timber.log('MyCutenessHistoryCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return
        else:
            userId = str(ctx.author.id)

        result = await self.__cutenessRepository.fetchCutenessHistory(
            twitchChannel = user.getHandle(),
            userId = userId,
            userName = userName
        )

        await twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessHistory(result, self.__delimiter))
        self.__timber.log('MyCutenessHistoryCommand', f'Handled !mycutenesshistory command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class PbsCommand(AbsCommand):

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

        if not user.hasSpeedrunProfile():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        speedrunProfile = user.getSpeedrunProfile()
        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s speedrun profile: {speedrunProfile}')
        self.__timber.log('PbsCommand', f'Handled !pbs command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
            mon = await self.__pokepediaRepository.searchPokemon(name)

            for string in mon.toStrList():
                await twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError) as e:
            self.__timber.log('PkMonCommand', f'Error retrieving Pokemon \"{name}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon \"{name}\"')

        self.__timber.log('PkMonCommand', f'Handled !pkmon command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
            move = await self.__pokepediaRepository.searchMoves(name)

            for string in move.toStrList():
                await twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError) as e:
            self.__timber.log('PkMoveCommand', f'Error retrieving Pokemon move: \"{name}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon move: \"{name}\"')

        self.__timber.log('PkMoveCommand', f'Handled !pkmove command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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


class SuperAnswerCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        usersRepository: UsersRepository
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameMachine is None:
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTriviaGameEnabled():
            return
        elif not self.__generalSettingsRepository.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() or not user.isSuperTriviaEnabled():
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        if len(splits) < 2:
            await twitchUtils.safeSend(ctx, '⚠ You must provide the exact answer with the !superanswer command.')
            return

        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckSuperAnswerTriviaAction(
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = str(ctx.author.id),
            userName = ctx.author.name
        ))

        self.__timber.log('SuperAnswerCommand', f'Handled !superanswer command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class SuperTriviaCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 2, seconds = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameMachine is None:
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: Context):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not self.__generalSettingsRepository.isTriviaEnabled():
            return
        elif not self.__generalSettingsRepository.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaEnabled() or not user.isSuperTriviaEnabled():
            return
        elif not ctx.author.is_mod or not ctx.author.name.lower() == user.getHandle().lower():
            return
        elif not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        points = self.__generalSettingsRepository.getTriviaGamePoints()
        if user.hasTriviaGamePoints():
            points = user.getTriviaGamePoints()

        multiplier = self.__generalSettingsRepository.getSuperTriviaGameMultiplier()
        if user.hasSuperTriviaGameMultiplier():
            multiplier = user.getSuperTriviaGameMultiplier()

        points = points * multiplier

        secondsToLive = self.__generalSettingsRepository.getWaitForSuperTriviaAnswerDelay()
        if user.hasWaitForSuperTriviaAnswerDelay():
            secondsToLive = user.getWaitForSuperTriviaAnswerDelay()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = user.getHandle(),
            areQuestionAnswerTriviaQuestionsEnabled = True,
            isJokeTriviaRepositoryEnabled = False,
            requireQuestionAnswerTriviaQuestion = True
        )

        self.__triviaGameMachine.submitAction(StartNewSuperTriviaGameAction(
            pointsMultiplier = multiplier,
            pointsForWinning = points,
            secondsToLive = secondsToLive,
            twitchChannel = user.getHandle(),
            triviaFetchOptions = triviaFetchOptions
        ))

        self.__timber.log('SuperTriviaCommand', f'Handled !supertrivia command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

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
            storeStock = await self.__tamaleGuyRepository.fetchStoreStock()
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
            response = await self.__translationHelper.translate(text, targetLanguageEntry)
            await twitchUtils.safeSend(ctx, response.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('TranslateCommand', f'Error translating text: \"{text}\": {e}')
            await twitchUtils.safeSend(ctx, '⚠ Error translating')

        self.__timber.log('TranslateCommand', f'Handled !translate command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                self.__timber.log('TriviaScoreCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await twitchUtils.safeSend(ctx, f'⚠ Unable to find user ID for \"{userName}\" in the database')
                return
        else:
            userId = str(ctx.author.id)

        triviaResult = await self.__triviaScoreRepository.fetchTriviaScore(
            twitchChannel = user.getHandle(),
            userId = userId
        )

        await twitchUtils.safeSend(ctx, self.__triviaUtils.getResults(userName, triviaResult))
        self.__timber.log('TriviaScoreCommand', f'Handled !triviascore command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


class TwitterCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
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

        if not user.hasTwitter():
            return
        elif not ctx.author.is_mod and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s twitter: {user.getTwitterUrl()}')
        self.__timber.log('TwitterCommand', f'Handled !twitter command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')


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

        location = await self.__locationsRepository.getLocation(user.getLocationId())

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(location)
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
            wotd = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await twitchUtils.safeSend(ctx, wotd.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\": {e}')
            await twitchUtils.safeSend(ctx, f'⚠ Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\"')

        self.__timber.log('WordCommand', f'Handled !word command for {ctx.author.name}:{ctx.author.id} in {user.getHandle()}')
