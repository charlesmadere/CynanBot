from asyncio import AbstractEventLoop
from typing import Any, Dict, Optional

from twitchio import Channel, Message
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound
from twitchio.ext.pubsub import PubSubChannelPointsMessage

import CynanBotCommon.utils as utils
from authRepository import AuthRepository
from commands import (AbsCommand, AddTriviaControllerCommand, AnalogueCommand,
                      AnswerCommand, BanTriviaQuestionCommand,
                      ClearCachesCommand, ClearSuperTriviaQueueCommand,
                      CommandsCommand, CutenessChampionsCommand,
                      CutenessCommand, CutenessHistoryCommand,
                      CynanSourceCommand, DiscordCommand,
                      GetTriviaControllersCommand, GiveCutenessCommand,
                      JishoCommand, LoremIpsumCommand, MyCutenessCommand,
                      MyCutenessHistoryCommand, PbsCommand, PkMonCommand,
                      PkMoveCommand, RaceCommand,
                      RemoveTriviaControllerCommand, StubCommand,
                      SuperAnswerCommand, SuperTriviaCommand, SwQuoteCommand,
                      TimeCommand, TranslateCommand, TriviaInfoCommand,
                      TriviaScoreCommand, TwitterCommand,
                      UnbanTriviaQuestionCommand, WeatherCommand, WordCommand)
from cutenessUtils import CutenessUtils
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.lruCache import LruCache
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBotCommon.trivia.bannedWordsRepository import BannedWordsRepository
from CynanBotCommon.trivia.clearedSuperTriviaQueueTriviaEvent import \
    ClearedSuperTriviaQueueTriviaEvent
from CynanBotCommon.trivia.correctAnswerTriviaEvent import \
    CorrectAnswerTriviaEvent
from CynanBotCommon.trivia.correctSuperAnswerTriviaEvent import \
    CorrectSuperAnswerTriviaEvent
from CynanBotCommon.trivia.failedToFetchQuestionSuperTriviaEvent import \
    FailedToFetchQuestionSuperTriviaEvent
from CynanBotCommon.trivia.failedToFetchQuestionTriviaEvent import \
    FailedToFetchQuestionTriviaEvent
from CynanBotCommon.trivia.incorrectAnswerTriviaEvent import \
    IncorrectAnswerTriviaEvent
from CynanBotCommon.trivia.invalidAnswerInputTriviaEvent import \
    InvalidAnswerInputTriviaEvent
from CynanBotCommon.trivia.newSuperTriviaGameEvent import \
    NewSuperTriviaGameEvent
from CynanBotCommon.trivia.newTriviaGameEvent import NewTriviaGameEvent
from CynanBotCommon.trivia.outOfTimeSuperTriviaEvent import \
    OutOfTimeSuperTriviaEvent
from CynanBotCommon.trivia.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from CynanBotCommon.trivia.tooLateToAnswerCheckAnswerTriviaEvent import \
    TooLateToAnswerCheckAnswerTriviaEvent
from CynanBotCommon.trivia.triviaBanHelper import TriviaBanHelper
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaEventListener import TriviaEventListener
from CynanBotCommon.trivia.triviaEventType import TriviaEventType
from CynanBotCommon.trivia.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from events import (AbsEvent, RaidLogEvent, RaidThankEvent, StubEvent,
                    SubGiftThankingEvent)
from generalSettingsRepository import GeneralSettingsRepository
from messages import (AbsMessage, CatJamMessage, ChatLogMessage, CynanMessage,
                      DeerForceMessage, EyesMessage, ImytSlurpMessage,
                      JamCatMessage, RatJamMessage, StubMessage)
from pointRedemptions import (AbsPointRedemption, CutenessRedemption,
                              PkmnBattleRedemption, PkmnCatchRedemption,
                              PkmnEvolveRedemption, PkmnShinyRedemption,
                              PotdPointRedemption, StubPointRedemption,
                              TriviaGameRedemption)
from triviaUtils import TriviaUtils
from twitch.eventSubUtils import EventSubUtils
from twitch.pubSubUtils import PubSubUtils
from twitch.twitchUtils import TwitchUtils
from users.usersRepository import UsersRepository


class CynanBot(commands.Bot, TriviaEventListener):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        analogueStoreRepository: Optional[AnalogueStoreRepository],
        authRepository: AuthRepository,
        bannedWordsRepository: Optional[BannedWordsRepository],
        chatLogger: Optional[ChatLogger],
        cutenessRepository: Optional[CutenessRepository],
        cutenessUtils: Optional[CutenessUtils],
        funtoonRepository: Optional[FuntoonRepository],
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: Optional[JishoHelper],
        languagesRepository: LanguagesRepository,
        locationsRepository: Optional[LocationsRepository],
        pokepediaRepository: Optional[PokepediaRepository],
        starWarsQuotesRepository: Optional[StarWarsQuotesRepository],
        timber: Timber,
        translationHelper: Optional[TranslationHelper],
        triviaBanHelper: Optional[TriviaBanHelper],
        triviaEmoteGenerator: Optional[TriviaEmoteGenerator],
        triviaGameControllersRepository: Optional[TriviaGameControllersRepository],
        triviaGameMachine: Optional[TriviaGameMachine],
        triviaHistoryRepository: Optional[TriviaHistoryRepository],
        triviaScoreRepository: Optional[TriviaScoreRepository],
        triviaSettingsRepository: Optional[TriviaSettingsRepository],
        triviaUtils: Optional[TriviaUtils],
        twitchTokensRepository: TwitchTokensRepository,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        weatherRepository: Optional[WeatherRepository],
        wordOfTheDayRepository: Optional[WordOfTheDayRepository]
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = [ user.getHandle().lower() for user in usersRepository.getUsers() ],
            loop = eventLoop,
            nick = authRepository.getAll().requireNick(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15
        )

        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(languagesRepository, LanguagesRepository):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepository):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__authRepository: AuthRepository = authRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

        self.__channelPointsLruCache: LruCache = LruCache(64)

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__commandsCommand: AbsCommand = CommandsCommand(generalSettingsRepository, timber, triviaUtils, twitchUtils, usersRepository)
        self.__cynanSourceCommand: AbsCommand = CynanSourceCommand(timber, twitchUtils, usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(timber, twitchUtils, usersRepository)
        self.__loremIpsumCommand: AbsCommand = LoremIpsumCommand(timber, twitchUtils, usersRepository)
        self.__pbsCommand: AbsCommand = PbsCommand(timber, twitchUtils, usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(timber, twitchUtils, usersRepository)
        self.__timeCommand: AbsCommand = TimeCommand(timber, twitchUtils, usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(timber, twitchUtils, usersRepository)

        if analogueStoreRepository is None:
            self.__analogueCommand: AbsCommand = StubCommand()
        else:
            self.__analogueCommand: AbsCommand = AnalogueCommand(analogueStoreRepository, generalSettingsRepository, timber, twitchUtils, usersRepository)

        if cutenessRepository is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__answerCommand: AbsCommand = StubCommand()
            self.__superAnswerCommand: AbsCommand = StubCommand()
            self.__superTriviaCommand: AbsCommand = StubCommand()
        else:
            self.__answerCommand: AbsCommand = AnswerCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)
            self.__superAnswerCommand: AbsCommand = SuperAnswerCommand(generalSettingsRepository, timber, triviaGameMachine, usersRepository)
            self.__superTriviaCommand: AbsCommand = SuperTriviaCommand(generalSettingsRepository, timber, triviaGameMachine, triviaUtils, twitchUtils, usersRepository)

        self.__clearCachesCommand: AbsCommand = ClearCachesCommand(analogueStoreRepository, authRepository, bannedWordsRepository, funtoonRepository, generalSettingsRepository, locationsRepository, timber, triviaSettingsRepository, twitchTokensRepository, twitchUtils, usersRepository, weatherRepository, wordOfTheDayRepository)

        if cutenessRepository is None or cutenessUtils is None:
            self.__cutenessCommand: AbsCommand = StubCommand()
            self.__cutenessChampionsCommand: AbsCommand = StubCommand()
            self.__cutenessHistoryCommand: AbsCommand = StubCommand()
            self.__giveCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessHistoryCommand: AbsCommand = StubCommand()
        else:
            self.__cutenessCommand: AbsCommand = CutenessCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__cutenessChampionsCommand: AbsCommand = CutenessChampionsCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__cutenessHistoryCommand: AbsCommand = CutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsCommand = GiveCutenessCommand(cutenessRepository, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__myCutenessCommand: AbsCommand = MyCutenessCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, usersRepository)
            self.__myCutenessHistoryCommand: AbsCommand = MyCutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsCommand = StubCommand()
        else:
            self.__jishoCommand: AbsCommand = JishoCommand(generalSettingsRepository, jishoHelper, timber, twitchUtils, usersRepository)

        if pokepediaRepository is None:
            self.__pkMonCommand: AbsCommand = StubCommand()
            self.__pkMoveCommand: AbsCommand = StubCommand()
        else:
            self.__pkMonCommand: AbsCommand = PkMonCommand(generalSettingsRepository, pokepediaRepository, timber, twitchUtils, usersRepository)
            self.__pkMoveCommand: AbsCommand = PkMoveCommand(generalSettingsRepository, pokepediaRepository, timber, twitchUtils, usersRepository)

        if starWarsQuotesRepository is None:
            self.__swQuoteCommand: AbsCommand = StubCommand()
        else:
            self.__swQuoteCommand: AbsCommand = SwQuoteCommand(starWarsQuotesRepository, timber, twitchUtils, usersRepository)

        if translationHelper is None:
            self.__translateCommand: AbsCommand = StubCommand()
        else:
            self.__translateCommand: AbsCommand = TranslateCommand(generalSettingsRepository, languagesRepository, timber, translationHelper, twitchUtils, usersRepository)

        if triviaGameControllersRepository is None or triviaUtils is None:
            self.__addTriviaControllerCommand: AbsCommand = StubCommand()
            self.__getTriviaControllersCommand: AbsCommand = StubCommand()
            self.__removeTriviaControllerCommand: AbsCommand = StubCommand()
        else:
            self.__addTriviaControllerCommand: AbsCommand = AddTriviaControllerCommand(generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)
            self.__getTriviaControllersCommand: AbsCommand = GetTriviaControllersCommand(generalSettingsRepository, timber, triviaGameControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__removeTriviaControllerCommand: AbsCommand = RemoveTriviaControllerCommand(generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)

        if triviaGameMachine is None or triviaUtils is None:
            self.__clearSuperTriviaQueueCommand: AbsCommand = StubCommand()
        else:
            self.__clearSuperTriviaQueueCommand: AbsCommand = ClearSuperTriviaQueueCommand(generalSettingsRepository, timber, triviaGameMachine, triviaUtils, usersRepository)

        if cutenessRepository is None or triviaBanHelper is None or triviaEmoteGenerator is None or triviaHistoryRepository is None or triviaScoreRepository is None or triviaUtils is None:
            self.__banTriviaQuestionCommand: AbsCommand = StubCommand()
            self.__triviaInfoCommand: AbsCommand = StubCommand()
            self.__triviaScoreCommand: AbsCommand = StubCommand()
            self.__unbanTriviaQuestionCommand: AbsCommand = StubCommand()
        else:
            self.__banTriviaQuestionCommand: AbsCommand = BanTriviaQuestionCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaInfoCommand: AbsCommand = TriviaInfoCommand(generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaScoreCommand: AbsCommand = TriviaScoreCommand(generalSettingsRepository, timber, triviaScoreRepository, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__unbanTriviaQuestionCommand: AbsCommand = UnbanTriviaQuestionCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)

        if locationsRepository is None or weatherRepository is None:
            self.__weatherCommand: AbsCommand = StubCommand()
        else:
            self.__weatherCommand: AbsCommand = WeatherCommand(generalSettingsRepository, locationsRepository, timber, twitchUtils, usersRepository, weatherRepository)

        if wordOfTheDayRepository is None:
            self.__wordCommand: AbsCommand = StubCommand()
        else:
            self.__wordCommand: AbsCommand = WordCommand(generalSettingsRepository, languagesRepository, timber, twitchUtils, usersRepository, wordOfTheDayRepository)

        #############################################
        ## Initialization of event handler objects ##
        #############################################

        if chatLogger is None:
            self.__raidLogEvent: AbsEvent = StubEvent()
        else:
            self.__raidLogEvent: AbsEvent = RaidLogEvent(chatLogger, timber)

        self.__raidThankEvent: AbsEvent = RaidThankEvent(generalSettingsRepository, timber, twitchUtils)
        self.__subGiftThankingEvent: AbsEvent = SubGiftThankingEvent(authRepository, generalSettingsRepository, timber, twitchUtils)

        ###############################################
        ## Initialization of message handler objects ##
        ###############################################

        self.__catJamMessage: AbsMessage = CatJamMessage(generalSettingsRepository, timber, twitchUtils)
        self.__cynanMessage: AbsMessage = CynanMessage(generalSettingsRepository, timber, twitchUtils)
        self.__deerForceMessage: AbsMessage = DeerForceMessage(generalSettingsRepository, timber, twitchUtils)
        self.__eyesMessage: AbsMessage = EyesMessage(generalSettingsRepository, timber, twitchUtils)
        self.__imytSlurpMessage: AbsMessage = ImytSlurpMessage(generalSettingsRepository, timber, twitchUtils)
        self.__jamCatMessage: AbsMessage = JamCatMessage(generalSettingsRepository, timber, twitchUtils)
        self.__ratJamMessage: AbsMessage = RatJamMessage(generalSettingsRepository, timber, twitchUtils)

        if chatLogger is None:
            self.__chatLogMessage: AbsMessage = StubMessage()
        else:
            self.__chatLogMessage: AbsMessage = ChatLogMessage(chatLogger)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

        self.__potdPointRedemption: AbsPointRedemption = PotdPointRedemption(timber, twitchUtils)

        if cutenessRepository is None:
            self.__cutenessPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsPointRedemption = CutenessRedemption(cutenessRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsPointRedemption = PkmnBattleRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnCatchPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnCatchPointRedemption: AbsPointRedemption = PkmnCatchRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnEvolvePointRedemption: AbsPointRedemption = PkmnEvolveRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnShinyPointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__pkmnShinyPointRedemption: AbsPointRedemption = PkmnShinyRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if cutenessRepository is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__triviaGamePointRedemption: AbsPointRedemption = StubPointRedemption()
        else:
            self.__triviaGamePointRedemption: AbsPointRedemption = TriviaGameRedemption(generalSettingsRepository, timber, triviaGameMachine)

        generalSettings = self.__generalSettingsRepository.getAll()

        ########################################
        ## Initialization of EventSub objects ##
        ########################################

        self.__eventSubUtils: Optional[EventSubUtils] = None
        if generalSettings.isEventSubEnabled():
            # TODO
            pass

        ######################################
        ## Initialization of PubSub objects ##
        ######################################

        self.__pubSubUtils: Optional[PubSubUtils] = None
        if generalSettings.isPubSubEnabled():
            self.__pubSubUtils = PubSubUtils(
                eventLoop = eventLoop,
                client = self,
                generalSettingsRepository = generalSettingsRepository,
                timber = timber,
                twitchCredentialsProviderInterface = authRepository,
                twitchTokensRepository = twitchTokensRepository,
                userIdsRepository = userIdsRepository,
                usersRepository = usersRepository
            )

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireNick()}')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message: Message):
        if message.echo:
            return

        if utils.isValidStr(message.content):
            generalSettings = await self.__generalSettingsRepository.getAllAsync()

            if generalSettings.isPersistAllUsersEnabled():
                await self.__userIdsRepository.setUser(
                    userId = str(message.author.id),
                    userName = message.author.name
                )

            twitchUser = await self.__usersRepository.getUserAsync(message.channel.name)

            await self.__chatLogMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            )

            if await self.__cynanMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__deerForceMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__catJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__imytSlurpMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__jamCatMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__ratJamMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

            if await self.__eyesMessage.handleMessage(
                twitchUser = twitchUser,
                message = message
            ):
                return

        await self.handle_commands(message)

    async def event_pubsub_channel_points(self, event: PubSubChannelPointsMessage):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        twitchUserIdStr = str(event.channel_id)
        twitchUserNameStr = await self.__userIdsRepository.fetchUserName(twitchUserIdStr)
        twitchUser = await self.__usersRepository.getUserAsync(twitchUserNameStr)
        rewardId = str(event.reward.id)
        userIdThatRedeemed = str(event.user.id)
        userNameThatRedeemed: str = event.user.name
        redemptionMessage: str = event.input
        lruCacheId = f'{twitchUserNameStr}:{event.id}'.lower()

        if generalSettings.isDebugLoggingEnabled() or generalSettings.isRewardIdPrintingEnabled() or twitchUser.isRewardIdPrintingEnabled():
            self.__timber.log('CynanBot', f'Reward ID for {twitchUser.getHandle()}:{twitchUserIdStr} (redeemed by {userNameThatRedeemed}:{userIdThatRedeemed}): \"{rewardId}\"')

        if self.__channelPointsLruCache.contains(lruCacheId):
            return

        self.__channelPointsLruCache.put(lruCacheId)
        twitchChannel = await self.__getChannel(twitchUser.getHandle())

        if generalSettings.isPersistAllUsersEnabled():
            await self.__userIdsRepository.setUser(
                userId = userIdThatRedeemed,
                userName = userNameThatRedeemed
            )

        if twitchUser.isCutenessEnabled() and twitchUser.hasCutenessBoosterPacks():
            if await self.__cutenessPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                return

        if twitchUser.isPicOfTheDayEnabled() and rewardId == twitchUser.getPicOfTheDayRewardId():
            if await self.__potdPointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                return

        if twitchUser.isPkmnEnabled():
            if rewardId == twitchUser.getPkmnBattleRewardId():
                if await self.__pkmnBattlePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

            if twitchUser.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

            if rewardId == twitchUser.getPkmnEvolveRewardId():
                if await self.__pkmnEvolvePointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

            if rewardId == twitchUser.getPkmnShinyRewardId():
                if await self.__pkmnShinyPointRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchUser = twitchUser,
                    redemptionMessage = redemptionMessage,
                    rewardId = rewardId,
                    userIdThatRedeemed = userIdThatRedeemed,
                    userNameThatRedeemed = userNameThatRedeemed
                ):
                    return

        if twitchUser.isTriviaGameEnabled() and rewardId == twitchUser.getTriviaGameRewardId():
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchUser = twitchUser,
                redemptionMessage = redemptionMessage,
                rewardId = rewardId,
                userIdThatRedeemed = userIdThatRedeemed,
                userNameThatRedeemed = userNameThatRedeemed
            ):
                return

    async def event_pubsub_error(self, tags: Dict):
        self.__timber.log('CynanBot', f'Received PubSub error: {tags}')

    async def event_pubsub_nonce(self, tags: Dict):
        self.__timber.log('CynanBot', f'Received PubSub nonce: {tags}')

    async def event_pubsub_pong(self):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if generalSettings.isPubSubPongLoggingEnabled():
            self.__timber.log('CynanBot', f'Received PubSub pong')

    async def event_raw_usernotice(self, channel: Channel, tags: Dict[str, Any]):
        if not utils.hasItems(tags):
            return

        msgId: Optional[str] = tags.get('msg-id')

        if not utils.isValidStr(msgId):
            return

        twitchUser = await self.__usersRepository.getUserAsync(channel.name)
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if msgId == 'raid':
            await self.__raidLogEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )

            await self.__raidThankEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )
        elif msgId == 'subgift' or msgId == 'anonsubgift':
            await self.__subGiftThankingEvent.handleEvent(
                twitchChannel = channel,
                twitchUser = twitchUser,
                tags = tags
            )
        elif generalSettings.isDebugLoggingEnabled():
            self.__timber.log('CynanBot', f'event_raw_usernotice(): {tags}')

    async def event_ready(self):
        authSnapshot = await self.__authRepository.getAllAsync()
        self.__timber.log('CynanBot', f'{authSnapshot.requireNick()} is ready!')

        if self.__triviaGameMachine is not None:
            self.__triviaGameMachine.setEventListener(self)

        if self.__eventSubUtils is not None:
            self.__eventSubUtils.startEventSub()

        if self.__pubSubUtils is not None:
            self.__pubSubUtils.startPubSub()

    async def __getChannel(self, twitchChannel: str) -> Channel:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.wait_for_ready()

        try:
            channel: Channel = self.get_channel(twitchChannel)

            if channel is None:
                self.__timber.log('CynanBot', f'Unable to get twitchChannel: \"{twitchChannel}\"')
                raise RuntimeError(f'Unable to get twitchChannel: \"{twitchChannel}\"')
            else:
                return channel
        except KeyError as e:
            self.__timber.log('CynanBot', f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e)
            raise RuntimeError(f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e)

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        triviaEventType = event.getTriviaEventType()
        self.__timber.log('CynanBot', f'Received new trivia event: \"{triviaEventType}\"')

        if triviaEventType is TriviaEventType.CLEARED_SUPER_TRIVIA_QUEUE:
            await self.__handleClearedSuperTriviaQueueTriviaEvent(event)
        elif triviaEventType is TriviaEventType.CORRECT_ANSWER:
            await self.__handleCorrectAnswerTriviaEvent(event)
        elif triviaEventType is TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionTriviaEvent(event)
        elif triviaEventType is TriviaEventType.GAME_OUT_OF_TIME:
            await self.__handleGameOutOfTimeTriviaEvent(event)
        elif triviaEventType is TriviaEventType.INCORRECT_ANSWER:
            await self.__handleIncorrectAnswerTriviaEvent(event)
        elif triviaEventType is TriviaEventType.INVALID_ANSWER_INPUT:
            await self.__handleInvalidAnswerInputTriviaEvent(event)
        elif triviaEventType is TriviaEventType.NEW_GAME:
            await self.__handleNewTriviaGameEvent(event)
        elif triviaEventType is TriviaEventType.NEW_SUPER_GAME:
            await self.__handleNewSuperTriviaGameEvent(event)
        elif triviaEventType is TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(event)
        elif triviaEventType is TriviaEventType.SUPER_GAME_CORRECT_ANSWER:
            await self.__handleSuperGameCorrectAnswerTriviaEvent(event)
        elif triviaEventType is TriviaEventType.SUPER_GAME_OUT_OF_TIME:
            await self.__handleSuperGameOutOfTimeTriviaEvent(event)
        elif triviaEventType is TriviaEventType.TOO_LATE_TO_ANSWER:
            await self.__handleTooLateToAnswerTriviaEvent(event)

    async def __handleClearedSuperTriviaQueueTriviaEvent(self, event: ClearedSuperTriviaQueueTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'ⓘ Cleared super trivia game queue ({event.getNumberOfGamesRemovedStr()} game(s) removed).')

    async def __handleCorrectAnswerTriviaEvent(self, event: CorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            newCuteness = event.getCutenessResult(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleFailedToFetchQuestionTriviaEvent(self, event: FailedToFetchQuestionTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch trivia question')

    async def __handleFailedToFetchQuestionSuperTriviaEvent(self, event: FailedToFetchQuestionSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch super trivia question')

    async def __handleGameOutOfTimeTriviaEvent(self, event: OutOfTimeTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleIncorrectAnswerTriviaEvent(self, event: IncorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleInvalidAnswerInputTriviaEvent(self, event: InvalidAnswerInputTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getInvalidAnswerInputPrompt(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleNewTriviaGameEvent(self, event: NewTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            userNameThatRedeemed = event.getUserName()
        ))

    async def __handleNewSuperTriviaGameEvent(self, event: NewSuperTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getSuperTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning()
        ))

    async def __handleSuperGameCorrectAnswerTriviaEvent(self, event: CorrectSuperAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            newCuteness = event.getCutenessResult(),
            points = event.getPointsForWinning(),
            userName = event.getUserName()
        ))

        launchpadPrompt = self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.getRemainingQueueSize()
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleSuperGameOutOfTimeTriviaEvent(self, event: OutOfTimeSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny()
        ))

        launchpadPrompt = self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.getRemainingQueueSize()
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleTooLateToAnswerTriviaEvent(self, event: TooLateToAnswerCheckAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            isShiny = event.isShiny(),
            userNameThatRedeemed = event.getUserName()
        ))

    @commands.command(name = 'a')
    async def command_a(self, ctx: Context):
        await self.__answerCommand.handleCommand(ctx)

    @commands.command(name = 'addtriviacontroller')
    async def command_addtriviacontroller(self, ctx: Context):
        await self.__addTriviaControllerCommand.handleCommand(ctx)

    @commands.command(name = 'analogue')
    async def command_analogue(self, ctx: Context):
        await self.__analogueCommand.handleCommand(ctx)

    @commands.command(name = 'answer')
    async def command_answer(self, ctx: Context):
        await self.__answerCommand.handleCommand(ctx)

    @commands.command(name = 'bantriviaquestion')
    async def command_bantriviaquestion(self, ctx: Context):
        await self.__banTriviaQuestionCommand.handleCommand(ctx)

    @commands.command(name = 'clearcaches')
    async def command_clearcaches(self, ctx: Context):
        await self.__clearCachesCommand.handleCommand(ctx)

    @commands.command(name = 'clearsupertriviaqueue')
    async def command_clearsupertriviaqueue(self, ctx: Context):
        await self.__clearSuperTriviaQueueCommand.handleCommand(ctx)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        await self.__commandsCommand.handleCommand(ctx)

    @commands.command(name = 'cuteness')
    async def command_cuteness(self, ctx: Context):
        await self.__cutenessCommand.handleCommand(ctx)

    @commands.command(name = 'cutenesschampions')
    async def command_cutenesschampions(self, ctx: Context):
        await self.__cutenessChampionsCommand.handleCommand(ctx)

    @commands.command(name = 'cutenesshistory')
    async def command_cutenesshistory(self, ctx: Context):
        await self.__cutenessHistoryCommand.handleCommand(ctx)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        await self.__cynanSourceCommand.handleCommand(ctx)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        await self.__discordCommand.handleCommand(ctx)

    @commands.command(name = 'gettriviacontrollers')
    async def command_gettriviacontrollers(self, ctx: Context):
        await self.__getTriviaControllersCommand.handleCommand(ctx)

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx: Context):
        await self.__giveCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        await self.__jishoCommand.handleCommand(ctx)

    @commands.command(name = 'lorem')
    async def command_lorem(self, ctx: Context):
        await self.__loremIpsumCommand.handleCommand(ctx)

    @commands.command(name = 'mycuteness')
    async def command_mycuteness(self, ctx: Context):
        await self.__myCutenessCommand.handleCommand(ctx)

    @commands.command(name = 'mycutenesshistory')
    async def command_mycutenesshistory(self, ctx: Context):
        await self.__myCutenessHistoryCommand.handleCommand(ctx)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx: Context):
        await self.__pbsCommand.handleCommand(ctx)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        await self.__pkMonCommand.handleCommand(ctx)

    @commands.command(name = 'pkmove')
    async def command_pkmove(self, ctx: Context):
        await self.__pkMoveCommand.handleCommand(ctx)

    @commands.command(name = 'race')
    async def command_race(self, ctx: Context):
        await self.__raceCommand.handleCommand(ctx)

    @commands.command(name = 'removetriviacontroller')
    async def command_removetriviacontroller(self, ctx: Context):
        await self.__removeTriviaControllerCommand.handleCommand(ctx)

    @commands.command(name = 'sa')
    async def command_sa(self, ctx: Context):
        await self.__superAnswerCommand.handleCommand(ctx)

    @commands.command(name = 'sanswer')
    async def command_sanswer(self, ctx: Context):
        await self.__superAnswerCommand.handleCommand(ctx)

    @commands.command(name = 'superanswer')
    async def command_superanswer(self, ctx: Context):
        await self.__superAnswerCommand.handleCommand(ctx)

    @commands.command(name = 'supertrivia')
    async def command_supertrivia(self, ctx: Context):
        await self.__superTriviaCommand.handleCommand(ctx)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        await self.__swQuoteCommand.handleCommand(ctx)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        await self.__timeCommand.handleCommand(ctx)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        await self.__translateCommand.handleCommand(ctx)

    @commands.command(name = 'triviainfo')
    async def command_triviainfo(self, ctx: Context):
        await self.__triviaInfoCommand.handleCommand(ctx)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        await self.__triviaScoreCommand.handleCommand(ctx)

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx: Context):
        await self.__twitterCommand.handleCommand(ctx)

    @commands.command(name = 'unbantriviaquestion')
    async def command_unbantriviaquestion(self, ctx: Context):
        await self.__unbanTriviaQuestionCommand.handleCommand(ctx)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        await self.__weatherCommand.handleCommand(ctx)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        await self.__wordCommand.handleCommand(ctx)
