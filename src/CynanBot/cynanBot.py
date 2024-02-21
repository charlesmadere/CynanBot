import traceback
from asyncio import AbstractEventLoop
from typing import Any, Dict, List, Optional

from twitchio import Channel, Message
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.authRepository import AuthRepository
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.channelPointRedemptions.casualGamePollRedemption import \
    CasualGamePollRedemption
from CynanBot.channelPointRedemptions.stubChannelPointRedemption import \
    StubPointRedemption
from CynanBot.chatActions.chatActionsManagerInterface import \
    ChatActionsManagerInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.chatCommands.addCheerActionCommand import AddCheerActionCommand
from CynanBot.chatCommands.stubChatCommand import StubChatCommand
from CynanBot.chatCommands.superAnswerChatCommand import SuperAnswerChatCommand
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBot.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.commands import (AbsCommand, AddBannedTriviaControllerCommand,
                               AddGlobalTriviaControllerCommand,
                               AddTriviaAnswerCommand,
                               AddTriviaControllerCommand, AddUserCommand,
                               AnswerCommand, BanTriviaQuestionCommand,
                               ClearCachesCommand,
                               ClearSuperTriviaQueueCommand, CommandsCommand,
                               ConfirmCommand, CutenessChampionsCommand,
                               CutenessCommand, CutenessHistoryCommand,
                               CynanSourceCommand, DeleteCheerActionCommand,
                               DeleteTriviaAnswersCommand, DiscordCommand,
                               GetBannedTriviaControllersCommand,
                               GetCheerActionsCommand,
                               GetGlobalTriviaControllersCommand,
                               GetTriviaAnswersCommand,
                               GetTriviaControllersCommand,
                               GiveCutenessCommand, JishoCommand,
                               LoremIpsumCommand, MyCutenessHistoryCommand,
                               PbsCommand, PkMonCommand, PkMoveCommand,
                               RaceCommand, RecurringActionCommand,
                               RecurringActionsCommand,
                               RemoveBannedTriviaControllerCommand,
                               RemoveGlobalTriviaControllerCommand,
                               RemoveTriviaControllerCommand,
                               SetFuntoonTokenCommand, SetTwitchCodeCommand,
                               StubCommand, SuperTriviaCommand, SwQuoteCommand,
                               TimeCommand, TranslateCommand,
                               TriviaInfoCommand, TriviaScoreCommand,
                               TtsCommand, TwitchInfoCommand, TwitterCommand,
                               UnbanTriviaQuestionCommand, WeatherCommand,
                               WordCommand)
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.dependencyHolder import DependencyHolder
from CynanBot.events import (AbsEvent, RaidLogEvent, RaidThankEvent, StubEvent,
                             SubGiftThankingEvent)
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.language.jishoHelperInterface import JishoHelperInterface
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translationHelper import TranslationHelper
from CynanBot.language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.pointRedemptions import (CutenessRedemption,
                                       PkmnBattleRedemption,
                                       PkmnCatchRedemption,
                                       PkmnEvolveRedemption,
                                       PkmnShinyRedemption,
                                       SuperTriviaGameRedemption,
                                       TriviaGameRedemption)
from CynanBot.recurringActions.recurringActionEventListener import \
    RecurringActionEventListener
from CynanBot.recurringActions.recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.recurringActions.recurringEvent import RecurringEvent
from CynanBot.recurringActions.recurringEventType import RecurringEventType
from CynanBot.recurringActions.superTriviaRecurringEvent import \
    SuperTriviaRecurringEvent
from CynanBot.recurringActions.weatherRecurringEvent import \
    WeatherRecurringEvent
from CynanBot.recurringActions.wordOfTheDayRecurringEvent import \
    WordOfTheDayRecurringEvent
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.starWars.starWarsQuotesRepositoryInterface import \
    StarWarsQuotesRepositoryInterface
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBot.trivia.banned.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.clearedSuperTriviaQueueTriviaEvent import \
    ClearedSuperTriviaQueueTriviaEvent
from CynanBot.trivia.events.correctAnswerTriviaEvent import \
    CorrectAnswerTriviaEvent
from CynanBot.trivia.events.correctSuperAnswerTriviaEvent import \
    CorrectSuperAnswerTriviaEvent
from CynanBot.trivia.events.failedToFetchQuestionSuperTriviaEvent import \
    FailedToFetchQuestionSuperTriviaEvent
from CynanBot.trivia.events.failedToFetchQuestionTriviaEvent import \
    FailedToFetchQuestionTriviaEvent
from CynanBot.trivia.events.incorrectAnswerTriviaEvent import \
    IncorrectAnswerTriviaEvent
from CynanBot.trivia.events.invalidAnswerInputTriviaEvent import \
    InvalidAnswerInputTriviaEvent
from CynanBot.trivia.events.newSuperTriviaGameEvent import \
    NewSuperTriviaGameEvent
from CynanBot.trivia.events.newTriviaGameEvent import NewTriviaGameEvent
from CynanBot.trivia.events.outOfTimeSuperTriviaEvent import \
    OutOfTimeSuperTriviaEvent
from CynanBot.trivia.events.outOfTimeTriviaEvent import OutOfTimeTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType
from CynanBot.trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from CynanBot.trivia.score.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from CynanBot.trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import \
    ShinyTriviaOccurencesRepositoryInterface
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import \
    ToxicTriviaOccurencesRepositoryInterface
from CynanBot.trivia.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from CynanBot.trivia.triviaEventListener import TriviaEventListener
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface
from CynanBot.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from CynanBot.twitch.absTwitchPollHandler import AbsTwitchPollHandler
from CynanBot.twitch.absTwitchPredictionHandler import \
    AbsTwitchPredictionHandler
from CynanBot.twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from CynanBot.twitch.absTwitchSubscriptionHandler import \
    AbsTwitchSubscriptionHandler
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.configuration.absChannelJoinEvent import \
    AbsChannelJoinEvent
from CynanBot.twitch.configuration.channelJoinEventType import \
    ChannelJoinEventType
from CynanBot.twitch.configuration.channelJoinHelper import ChannelJoinHelper
from CynanBot.twitch.configuration.channelJoinListener import \
    ChannelJoinListener
from CynanBot.twitch.configuration.finishedJoiningChannelsEvent import \
    FinishedJoiningChannelsEvent
from CynanBot.twitch.configuration.joinChannelsEvent import JoinChannelsEvent
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointRedemptionHandler import \
    TwitchChannelPointRedemptionHandler
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.configuration.twitchConfiguration import \
    TwitchConfiguration
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchCheerHandler import TwitchCheerHandler
from CynanBot.twitch.twitchFollowerRepositoryInterface import \
    TwitchFollowerRepositoryInterface
from CynanBot.twitch.twitchPollHandler import TwitchPollHandler
from CynanBot.twitch.twitchPredictionHandler import TwitchPredictionHandler
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.twitchRaidHandler import TwitchRaidHandler
from CynanBot.twitch.twitchSubscriptionHandler import TwitchSubscriptionHandler
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchTokensUtilsInterface import \
    TwitchTokensUtilsInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.twitch.twitchWebsocketDataBundleHandler import \
    TwitchWebsocketDataBundleHandler
from CynanBot.twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from CynanBot.users.modifyUserActionType import ModifyUserActionType
from CynanBot.users.modifyUserData import ModifyUserData
from CynanBot.users.modifyUserDataHelper import ModifyUserDataHelper
from CynanBot.users.modifyUserEventListener import ModifyUserEventListener
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class CynanBot(commands.Bot, ChannelJoinListener, ModifyUserEventListener, RecurringActionEventListener, \
    TriviaEventListener, TwitchChannelProvider):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        additionalTriviaAnswersRepository: Optional[AdditionalTriviaAnswersRepositoryInterface],
        administratorProvider: AdministratorProviderInterface,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelper,
        bannedTriviaGameControllersRepository: Optional[BannedTriviaGameControllersRepositoryInterface],
        bannedWordsRepository: Optional[BannedWordsRepositoryInterface],
        channelJoinHelper: ChannelJoinHelper,
        chatActionsManager: Optional[ChatActionsManagerInterface],
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: Optional[CheerActionHelperInterface],
        cheerActionIdGenerator: Optional[CheerActionIdGeneratorInterface],
        cheerActionRemodHelper: Optional[CheerActionRemodHelperInterface],
        cheerActionsRepository: Optional[CheerActionsRepositoryInterface],
        cutenessRepository: Optional[CutenessRepositoryInterface],
        cutenessUtils: Optional[CutenessUtilsInterface],
        dependencyHolder: DependencyHolder,
        funtoonRepository: Optional[FuntoonRepositoryInterface],
        funtoonTokensRepository: Optional[FuntoonTokensRepositoryInterface],
        generalSettingsRepository: GeneralSettingsRepository,
        isLiveOnTwitchRepository: Optional[IsLiveOnTwitchRepositoryInterface],
        jishoHelper: Optional[JishoHelperInterface],
        languagesRepository: LanguagesRepositoryInterface,
        locationsRepository: Optional[LocationsRepositoryInterface],
        modifyUserDataHelper: ModifyUserDataHelper,
        mostRecentChatsRepository: Optional[MostRecentChatsRepositoryInterface],
        openTriviaDatabaseTriviaQuestionRepository: Optional[OpenTriviaDatabaseTriviaQuestionRepository],
        pokepediaRepository: Optional[PokepediaRepository],
        recurringActionsMachine: Optional[RecurringActionsMachineInterface],
        recurringActionsRepository: Optional[RecurringActionsRepositoryInterface],
        sentMessageLogger: SentMessageLoggerInterface,
        shinyTriviaOccurencesRepository: Optional[ShinyTriviaOccurencesRepositoryInterface],
        soundPlayerSettingsRepository: Optional[SoundPlayerSettingsRepositoryInterface],
        starWarsQuotesRepository: Optional[StarWarsQuotesRepositoryInterface],
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface,
        toxicTriviaOccurencesRepository: Optional[ToxicTriviaOccurencesRepositoryInterface],
        translationHelper: Optional[TranslationHelper],
        triviaBanHelper: Optional[TriviaBanHelperInterface],
        triviaEmoteGenerator: Optional[TriviaEmoteGeneratorInterface],
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameControllersRepository: Optional[TriviaGameControllersRepositoryInterface],
        triviaGameGlobalControllersRepository: Optional[TriviaGameGlobalControllersRepositoryInterface],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        triviaHistoryRepository: Optional[TriviaHistoryRepositoryInterface],
        triviaIdGenerator: Optional[TriviaIdGeneratorInterface],
        triviaRepository: Optional[TriviaRepositoryInterface],
        triviaScoreRepository: Optional[TriviaScoreRepositoryInterface],
        triviaSettingsRepository: Optional[TriviaSettingsRepositoryInterface],
        triviaUtils: Optional[TriviaUtilsInterface],
        ttsSettingsRepository: Optional[TtsSettingsRepositoryInterface],
        twitchApiService: TwitchApiServiceInterface,
        twitchConfiguration: TwitchConfiguration,
        twitchFollowerRepository: Optional[TwitchFollowerRepositoryInterface],
        twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface],
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        twitchWebsocketClient: Optional[TwitchWebsocketClientInterface],
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: Optional[WeatherRepositoryInterface],
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface],
        wordOfTheDayRepository: Optional[WordOfTheDayRepositoryInterface]
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = list(),
            loop = eventLoop,
            nick = authRepository.getAll().requireTwitchHandle(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15
        )

        assert isinstance(eventLoop, AbstractEventLoop), f"malformed {eventLoop=}"
        assert additionalTriviaAnswersRepository is None or isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(authRepository, AuthRepository), f"malformed {authRepository=}"
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert bannedTriviaGameControllersRepository is None or isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface), f"malformed {bannedTriviaGameControllersRepository=}"
        assert bannedWordsRepository is None or isinstance(bannedWordsRepository, BannedWordsRepositoryInterface), f"malformed {bannedWordsRepository=}"
        assert isinstance(channelJoinHelper, ChannelJoinHelper), f"malformed {channelJoinHelper=}"
        assert chatActionsManager is None or isinstance(chatActionsManager, ChatActionsManagerInterface), f"malformed {chatActionsManager=}"
        assert isinstance(chatLogger, ChatLoggerInterface), f"malformed {chatLogger=}"
        assert cheerActionHelper is None or isinstance(cheerActionHelper, CheerActionHelperInterface), f"malformed {cheerActionHelper=}"
        assert cheerActionIdGenerator is None or isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface), f"malformed {cheerActionIdGenerator=}"
        assert cheerActionRemodHelper is None or isinstance(cheerActionRemodHelper, CheerActionRemodHelperInterface), f"malformed {cheerActionRemodHelper=}"
        assert cheerActionsRepository is None or isinstance(cheerActionsRepository, CheerActionsRepositoryInterface), f"malformed {cheerActionsRepository=}"
        assert cutenessRepository is None or isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert cutenessUtils is None or isinstance(cutenessUtils, CutenessUtilsInterface), f"malformed {cutenessUtils=}"
        assert isinstance(dependencyHolder, DependencyHolder), f"malformed {dependencyHolder=}"
        assert funtoonRepository is None or isinstance(funtoonRepository, FuntoonRepositoryInterface), f"malformed {funtoonRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isLiveOnTwitchRepository is None or isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface), f"malformed {isLiveOnTwitchRepository=}"
        assert jishoHelper is None or isinstance(jishoHelper, JishoHelperInterface), f"malformed {jishoHelper=}"
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert locationsRepository is None or isinstance(locationsRepository, LocationsRepositoryInterface), f"malformed {locationsRepository=}"
        assert isinstance(modifyUserDataHelper, ModifyUserDataHelper), f"malformed {modifyUserDataHelper=}"
        assert mostRecentChatsRepository is None or isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface), f"malformed {mostRecentChatsRepository=}"
        assert openTriviaDatabaseTriviaQuestionRepository is None or isinstance(openTriviaDatabaseTriviaQuestionRepository, OpenTriviaDatabaseTriviaQuestionRepository), f"malformed {openTriviaDatabaseTriviaQuestionRepository=}"
        assert pokepediaRepository is None or isinstance(pokepediaRepository, PokepediaRepository), f"malformed {pokepediaRepository=}"
        assert recurringActionsMachine is None or isinstance(recurringActionsMachine, RecurringActionsMachineInterface), f"malformed {recurringActionsMachine=}"
        assert recurringActionsRepository is None or isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface), f"malformed {recurringActionsRepository=}"
        assert isinstance(sentMessageLogger, SentMessageLoggerInterface), f"malformed {sentMessageLogger=}"
        assert shinyTriviaOccurencesRepository is None or isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface), f"malformed {shinyTriviaOccurencesRepository=}"
        assert soundPlayerSettingsRepository is None or isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface), f"malformed {soundPlayerSettingsRepository=}"
        assert starWarsQuotesRepository is None or isinstance(starWarsQuotesRepository, StarWarsQuotesRepositoryInterface), f"malformed {starWarsQuotesRepository=}"
        assert streamAlertsManager is None or isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert toxicTriviaOccurencesRepository is None or isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface), f"malformed {toxicTriviaOccurencesRepository=}"
        assert translationHelper is None or isinstance(translationHelper, TranslationHelper), f"malformed {translationHelper=}"
        assert triviaBanHelper is None or isinstance(triviaBanHelper, TriviaBanHelperInterface), f"malformed {triviaBanHelper=}"
        assert triviaEmoteGenerator is None or isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert triviaGameBuilder is None or isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert triviaGameControllersRepository is None or isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface), f"malformed {triviaGameControllersRepository=}"
        assert triviaGameGlobalControllersRepository is None or isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface), f"malformed {triviaGameGlobalControllersRepository=}"
        assert triviaGameMachine is None or isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert triviaHistoryRepository is None or isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert triviaIdGenerator is None or isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert triviaRepository is None or isinstance(triviaRepository, TriviaRepositoryInterface), f"malformed {triviaRepository=}"
        assert triviaScoreRepository is None or isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface), f"malformed {triviaScoreRepository=}"
        assert triviaSettingsRepository is None or isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"
        assert triviaUtils is None or isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert ttsSettingsRepository is None or isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface), f"malformed {ttsSettingsRepository=}"
        assert isinstance(twitchApiService, TwitchApiServiceInterface), f"malformed {twitchApiService=}"
        assert isinstance(twitchConfiguration, TwitchConfiguration), f"malformed {twitchConfiguration=}"
        assert twitchFollowerRepository is None or isinstance(twitchFollowerRepository, TwitchFollowerRepositoryInterface), f"malformed {twitchFollowerRepository=}"
        assert twitchPredictionWebsocketUtils is None or isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface), f"malformed {twitchPredictionWebsocketUtils=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchTokensUtils, TwitchTokensUtilsInterface), f"malformed {twitchTokensUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert twitchWebsocketClient is None or isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface), f"malformed {twitchWebsocketClient=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert weatherRepository is None or isinstance(weatherRepository, WeatherRepositoryInterface), f"malformed {weatherRepository=}"
        assert websocketConnectionServer is None or isinstance(websocketConnectionServer, WebsocketConnectionServerInterface), f"malformed {websocketConnectionServer=}"
        assert wordOfTheDayRepository is None or isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface), f"malformed {wordOfTheDayRepository=}"

        self.__authRepository: AuthRepository = authRepository
        self.__channelJoinHelper: ChannelJoinHelper = channelJoinHelper
        self.__chatActionsManager: Optional[ChatActionsManagerInterface] = chatActionsManager
        self.__cheerActionHelper: Optional[CheerActionHelperInterface] = cheerActionHelper
        self.__cheerActionRemodHelper: Optional[CheerActionRemodHelperInterface] = cheerActionRemodHelper
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__recurringActionsMachine: Optional[RecurringActionsMachineInterface] = recurringActionsMachine
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: Optional[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Optional[TriviaGameMachineInterface] = triviaGameMachine
        self.__triviaRepository: Optional[TriviaRepositoryInterface] = triviaRepository
        self.__triviaUtils: Optional[TriviaUtilsInterface] = triviaUtils
        self.__twitchConfiguration: TwitchConfiguration = twitchConfiguration
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = twitchPredictionWebsocketUtils
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__twitchWebsocketClient: Optional[TwitchWebsocketClientInterface] = twitchWebsocketClient
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = websocketConnectionServer

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__addUserCommand: AbsCommand = AddUserCommand(administratorProvider, modifyUserDataHelper, timber, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository)
        self.__clearCachesCommand: AbsCommand = ClearCachesCommand(administratorProvider, authRepository, bannedWordsRepository, cheerActionsRepository, funtoonTokensRepository, generalSettingsRepository, isLiveOnTwitchRepository, locationsRepository, modifyUserDataHelper, mostRecentChatsRepository, openTriviaDatabaseTriviaQuestionRepository, soundPlayerSettingsRepository, timber, triviaSettingsRepository, ttsSettingsRepository, twitchFollowerRepository, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository, weatherRepository, websocketConnectionServer, wordOfTheDayRepository)
        self.__commandsCommand: AbsCommand = CommandsCommand(generalSettingsRepository, timber, triviaUtils, twitchUtils, usersRepository)
        self.__confirmCommand: AbsCommand = ConfirmCommand(administratorProvider, modifyUserDataHelper, timber, twitchUtils, usersRepository)
        self.__cynanSourceCommand: AbsCommand = CynanSourceCommand(timber, twitchUtils, usersRepository)
        self.__discordCommand: AbsCommand = DiscordCommand(timber, twitchUtils, usersRepository)
        self.__loremIpsumCommand: AbsCommand = LoremIpsumCommand(timber, twitchUtils, usersRepository)
        self.__mastodonCommand: AbsCommand = StubCommand()
        self.__pbsCommand: AbsCommand = PbsCommand(timber, twitchUtils, usersRepository)
        self.__raceCommand: AbsCommand = RaceCommand(timber, twitchUtils, usersRepository)
        self.__setTwitchCodeCommand: AbsCommand = SetTwitchCodeCommand(administratorProvider, timber, twitchTokensRepository, twitchUtils, usersRepository)
        self.__timeCommand: AbsCommand = TimeCommand(timber, twitchUtils, usersRepository)
        self.__twitchInfoCommand: AbsCommand = TwitchInfoCommand(administratorProvider, timber, twitchApiService, authRepository, twitchTokensRepository, twitchUtils, usersRepository)
        self.__twitterCommand: AbsCommand = TwitterCommand(timber, twitchUtils, usersRepository)

        if cheerActionHelper is None or cheerActionIdGenerator is None or cheerActionsRepository is None:
            self.__addCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__deleteCheerActionCommand: AbsCommand = StubCommand()
            self.__getCheerActionsCommand: AbsCommand = StubCommand()
        else:
            self.__addCheerActionCommand: AbsChatCommand = AddCheerActionCommand(administratorProvider, cheerActionsRepository, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__deleteCheerActionCommand: AbsCommand = DeleteCheerActionCommand(administratorProvider, cheerActionIdGenerator, cheerActionsRepository, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__getCheerActionsCommand: AbsCommand = GetCheerActionsCommand(administratorProvider, cheerActionsRepository, timber, twitchUtils, userIdsRepository, usersRepository)

        if recurringActionsMachine is None or recurringActionsRepository is None:
            self.__recurringActionCommand: AbsCommand = StubCommand()
            self.__recurringActionsCommand: AbsCommand = StubCommand()
        else:
            self.__recurringActionCommand: AbsCommand = RecurringActionCommand(administratorProvider, languagesRepository, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__recurringActionsCommand: AbsCommand = RecurringActionsCommand(administratorProvider, recurringActionsRepository, timber, twitchUtils, usersRepository)

        if bannedTriviaGameControllersRepository is None or triviaUtils is None:
            self.__addBannedTriviaControllerCommand: AbsCommand = StubCommand()
            self.__getBannedTriviaControllersCommand: AbsCommand = StubCommand()
            self.__removeBannedTriviaControllerCommand: AbsCommand = StubCommand()
        else:
            self.__addBannedTriviaControllerCommand: AbsCommand = AddBannedTriviaControllerCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchUtils, usersRepository)
            self.__getBannedTriviaControllersCommand: AbsCommand = GetBannedTriviaControllersCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, triviaUtils, twitchUtils, usersRepository)
            self.__removeBannedTriviaControllerCommand: AbsCommand = RemoveBannedTriviaControllerCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchUtils, usersRepository)

        if triviaGameGlobalControllersRepository is None or triviaUtils is None:
            self.__addGlobalTriviaControllerCommand: AbsCommand = StubCommand()
            self.__getGlobalTriviaControllersCommand: AbsCommand = StubCommand()
            self.__removeGlobalTriviaControllerCommand: AbsCommand = StubCommand()
        else:
            self.__addGlobalTriviaControllerCommand: AbsCommand = AddGlobalTriviaControllerCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchUtils, usersRepository)
            self.__getGlobalTriviaControllersCommand: AbsCommand = GetGlobalTriviaControllersCommand(administratorProvider,  timber, triviaGameGlobalControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__removeGlobalTriviaControllerCommand: AbsCommand = RemoveGlobalTriviaControllerCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchUtils, usersRepository)

        if additionalTriviaAnswersRepository is None or cutenessRepository is None or triviaEmoteGenerator is None or triviaGameBuilder is None or triviaGameMachine is None or triviaHistoryRepository is None or triviaIdGenerator is None or triviaSettingsRepository is None or triviaScoreRepository is None or triviaUtils is None:
            self.__addTriviaAnswerCommand: AbsCommand = StubCommand()
            self.__answerCommand: AbsCommand = StubCommand()
            self.__deleteTriviaAnswersCommand: AbsCommand = StubCommand()
            self.__getTriviaAnswersCommand: AbsCommand = StubCommand()
            self.__superAnswerCommand: AbsChatCommand = StubChatCommand()
            self.__superTriviaCommand: AbsCommand = StubCommand()
        else:
            self.__addTriviaAnswerCommand: AbsCommand = AddTriviaAnswerCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__answerCommand: AbsCommand = AnswerCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, usersRepository)
            self.__deleteTriviaAnswersCommand: AbsCommand = DeleteTriviaAnswersCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__getTriviaAnswersCommand: AbsCommand = GetTriviaAnswersCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__superAnswerCommand: AbsChatCommand = SuperAnswerChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, usersRepository)
            self.__superTriviaCommand: AbsCommand = SuperTriviaCommand(generalSettingsRepository, timber, triviaGameBuilder, triviaGameMachine, triviaSettingsRepository, triviaUtils, twitchUtils, usersRepository)

        if cutenessRepository is None or cutenessUtils is None or triviaUtils is None:
            self.__cutenessCommand: AbsCommand = StubCommand()
            self.__cutenessChampionsCommand: AbsCommand = StubCommand()
            self.__cutenessHistoryCommand: AbsCommand = StubCommand()
            self.__giveCutenessCommand: AbsCommand = StubCommand()
            self.__myCutenessHistoryCommand: AbsCommand = StubCommand()
        else:
            self.__cutenessCommand: AbsCommand = CutenessCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__cutenessChampionsCommand: AbsCommand = CutenessChampionsCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, usersRepository)
            self.__cutenessHistoryCommand: AbsCommand = CutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsCommand = GiveCutenessCommand(cutenessRepository, timber, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__myCutenessHistoryCommand: AbsCommand = MyCutenessHistoryCommand(cutenessRepository, cutenessUtils, timber, twitchUtils, userIdsRepository, usersRepository)

        if funtoonTokensRepository is None:
            self.__setFuntoonTokenCommand: AbsCommand = StubCommand()
        else:
            self.__setFuntoonTokenCommand: AbsCommand = SetFuntoonTokenCommand(administratorProvider, funtoonTokensRepository, timber, twitchUtils, usersRepository)

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
            self.__addTriviaControllerCommand: AbsCommand = AddTriviaControllerCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)
            self.__getTriviaControllersCommand: AbsCommand = GetTriviaControllersCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, triviaUtils, twitchUtils, usersRepository)
            self.__removeTriviaControllerCommand: AbsCommand = RemoveTriviaControllerCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchUtils, usersRepository)

        if triviaGameMachine is None or triviaIdGenerator is None or triviaUtils is None:
            self.__clearSuperTriviaQueueCommand: AbsCommand = StubCommand()
        else:
            self.__clearSuperTriviaQueueCommand: AbsCommand = ClearSuperTriviaQueueCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, triviaUtils, usersRepository)

        if additionalTriviaAnswersRepository is None or cutenessRepository is None or shinyTriviaOccurencesRepository is None or toxicTriviaOccurencesRepository is None or triviaBanHelper is None or triviaEmoteGenerator is None or triviaHistoryRepository is None or triviaScoreRepository is None or triviaUtils is None:
            self.__banTriviaQuestionCommand: AbsCommand = StubCommand()
            self.__triviaInfoCommand: AbsCommand = StubCommand()
            self.__triviaScoreCommand: AbsCommand = StubCommand()
            self.__unbanTriviaQuestionCommand: AbsCommand = StubCommand()
        else:
            self.__banTriviaQuestionCommand: AbsCommand = BanTriviaQuestionCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaInfoCommand: AbsCommand = TriviaInfoCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)
            self.__triviaScoreCommand: AbsCommand = TriviaScoreCommand(generalSettingsRepository, shinyTriviaOccurencesRepository, timber, toxicTriviaOccurencesRepository, triviaScoreRepository, triviaUtils, twitchUtils, userIdsRepository, usersRepository)
            self.__unbanTriviaQuestionCommand: AbsCommand = UnbanTriviaQuestionCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)

        if streamAlertsManager is None:
            self.__ttsCommand: AbsCommand = StubCommand()
        else:
            self.__ttsCommand: AbsCommand = TtsCommand(administratorProvider, streamAlertsManager, timber, twitchUtils, usersRepository)

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
        self.__subGiftThankingEvent: AbsEvent = SubGiftThankingEvent(generalSettingsRepository, timber, authRepository, twitchUtils)

        ########################################################
        ## Initialization of point redemption handler objects ##
        ########################################################

        self.__casualGamePollPointRedemption: AbsChannelPointRedemption = CasualGamePollRedemption(timber, twitchUtils)

        if cutenessRepository is None:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__cutenessPointRedemption: AbsChannelPointRedemption = CutenessRedemption(cutenessRepository, timber, twitchUtils)

        if funtoonRepository is None:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__pkmnBattlePointRedemption: AbsChannelPointRedemption = PkmnBattleRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnCatchPointRedemption: AbsChannelPointRedemption = PkmnCatchRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnEvolvePointRedemption: AbsChannelPointRedemption = PkmnEvolveRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)
            self.__pkmnShinyPointRedemption: AbsChannelPointRedemption = PkmnShinyRedemption(funtoonRepository, generalSettingsRepository, timber, twitchUtils)

        if cutenessRepository is None or triviaGameBuilder is None or triviaGameMachine is None or triviaScoreRepository is None or triviaUtils is None:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = StubPointRedemption()
        else:
            self.__superTriviaGamePointRedemption: AbsChannelPointRedemption = SuperTriviaGameRedemption(timber, triviaGameBuilder, triviaGameMachine)
            self.__triviaGamePointRedemption: AbsChannelPointRedemption = TriviaGameRedemption(timber, triviaGameBuilder, triviaGameMachine)

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireTwitchHandle()}')

    async def event_channel_join_failure(self, channel: str):
        userId = await self.__userIdsRepository.fetchUserId(channel)
        user: Optional[UserInterface] = None

        try:
            user = await self.__usersRepository.getUserAsync(channel)
        except:
            pass

        self.__timber.log('CynanBot', f'Failed to join channel \"{channel}\" (userId=\"{userId}\") (user=\"{user}\"), disabling this user...')

        await self.__usersRepository.setUserEnabled(
            handle = user.getHandle(),
            enabled = False
        )

        self.__timber.log('CynanBot', f'Finished disabling user \"{user}\" due to channel join failure')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_message(self, message: Message):
        if message.echo:
            return

        twitchMessage = self.__twitchConfiguration.getMessage(message)

        if self.__chatActionsManager is not None:
            await self.__chatActionsManager.handleMessage(twitchMessage)

        await self.handle_commands(message)

    async def event_raw_usernotice(self, channel: Channel, tags: Dict[str, Any]):
        twitchChannel = self.__twitchConfiguration.getChannel(channel)
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isDebugLoggingEnabled():
            self.__timber.log('CynanBot', f'event_raw_usernotice(): (channel=\"{twitchChannel}\") (tags=\"{tags}\")')

        msgId = utils.getStrFromDict(tags, 'msg-id', fallback = '')

        if not utils.isValidStr(msgId):
            return

        twitchUser = await self.__usersRepository.getUserAsync(channel.name)

        if msgId == 'raid':
            await self.__raidLogEvent.handleEvent(
                channel = twitchChannel,
                user = twitchUser,
                tags = tags
            )

            await self.__raidThankEvent.handleEvent(
                channel = twitchChannel,
                user = twitchUser,
                tags = tags
            )
        elif msgId == 'subgift' or msgId == 'anonsubgift':
            await self.__subGiftThankingEvent.handleEvent(
                channel = twitchChannel,
                user = twitchUser,
                tags = tags
            )

    async def event_ready(self):
        await self.wait_for_ready()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBot', f'{twitchHandle} is ready!')

        self.__channelJoinHelper.setChannelJoinListener(self)
        self.__channelJoinHelper.joinChannels()
        self.__modifyUserDataHelper.setModifyUserEventListener(self)

    async def event_reconnect(self):
        self.__timber.log('CynanBot', f'Received new reconnect event')
        await self.wait_for_ready()
        self.__timber.log('CynanBot', f'Finished reconnecting')

    async def event_usernotice_subscription(self, metadata):
        self.__timber.log('CynanBot', f'event_usernotice_subscription(): (metadata=\"{metadata}\")')

    async def __getChannel(self, twitchChannel: str) -> TwitchChannel:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.wait_for_ready()

        try:
            channel = self.get_channel(twitchChannel)

            if channel is None:
                self.__timber.log('CynanBot', f'Unable to get twitchChannel: \"{twitchChannel}\"')
                raise RuntimeError(f'Unable to get twitchChannel: \"{twitchChannel}\"')
            else:
                return self.__twitchConfiguration.getChannel(channel)
        except KeyError as e:
            self.__timber.log('CynanBot', f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())

    async def getTwitchChannel(self, twitchChannel: str) -> TwitchChannel:
        return await self.__getChannel(twitchChannel)

    async def onModifyUserEvent(self, event: ModifyUserData):
        self.__timber.log('CynanBot', f'Received new modify user data event: {event.toStr()}')

        await self.wait_for_ready()

        if event.getActionType() is ModifyUserActionType.ADD:
            channels: List[str] = list()
            channels.append(event.getUserName())
            await self.join_channels(channels)
        elif event.getActionType() is ModifyUserActionType.REMOVE:
            channels: List[str] = list()
            channels.append(event.getUserName())
            await self.part_channels(channels)
        else:
            raise RuntimeError(f'unknown ModifyUserActionType: \"{event.getActionType()}\"')

    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        eventType = event.getEventType()
        self.__timber.log('CynanBot', f'Received new channel join event: \"{eventType}\"')

        await self.wait_for_ready()

        if eventType is ChannelJoinEventType.FINISHED:
            await self.__handleFinishedJoiningChannelsEvent(event)
        elif eventType is ChannelJoinEventType.JOIN:
            await self.__handleJoinChannelsEvent(event)

    async def __handleFinishedJoiningChannelsEvent(self, event: FinishedJoiningChannelsEvent):
        self.__timber.log('CynanBot', f'Finished joining channels: {event.getAllChannels()}')

        self.__sentMessageLogger.start()
        self.__chatLogger.start()
        self.__twitchUtils.start()

        if self.__streamAlertsManager is not None:
            self.__streamAlertsManager.start()

        if self.__cheerActionRemodHelper is not None:
            self.__cheerActionRemodHelper.start()

        if self.__triviaRepository is not None:
            self.__triviaRepository.startSpooler()

        if self.__triviaGameMachine is not None:
            self.__triviaGameMachine.setEventListener(self)
            self.__triviaGameMachine.startMachine()

        if self.__recurringActionsMachine is not None:
            self.__recurringActionsMachine.setEventListener(self)
            self.__recurringActionsMachine.startMachine()

        if self.__websocketConnectionServer is not None:
            self.__websocketConnectionServer.start()

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isEventSubEnabled() and self.__twitchWebsocketClient is not None:
            cheerHandler: Optional[AbsTwitchCheerHandler] = TwitchCheerHandler(
                cheerActionHelper = self.__cheerActionHelper,
                streamAlertsManager = self.__streamAlertsManager,
                timber = self.__timber,
                triviaGameBuilder = self.__triviaGameBuilder,
                triviaGameMachine = self.__triviaGameMachine,
                twitchChannelProvider = self
            )

            pollHandler: Optional[AbsTwitchPollHandler] = TwitchPollHandler(
                streamAlertsManager = self.__streamAlertsManager,
                timber = self.__timber
            )

            predictionHandler: Optional[AbsTwitchPredictionHandler] = TwitchPredictionHandler(
                streamAlertsManager = self.__streamAlertsManager,
                timber = self.__timber,
                twitchPredictionWebsocketUtils = self.__twitchPredictionWebsocketUtils,
                websocketConnectionServer = self.__websocketConnectionServer
            )

            raidHandler: Optional[AbsTwitchRaidHandler] = TwitchRaidHandler(
                streamAlertsManager = self.__streamAlertsManager,
                timber = self.__timber
            )

            subscriptionHandler: Optional[AbsTwitchSubscriptionHandler] = TwitchSubscriptionHandler(
                streamAlertsManager = self.__streamAlertsManager,
                timber = self.__timber,
                triviaGameBuilder = self.__triviaGameBuilder,
                triviaGameMachine = self.__triviaGameMachine,
                twitchChannelProvider = self,
                twitchTokensUtils = self.__twitchTokensUtils,
                userIdsRepository = self.__userIdsRepository
            )

            self.__twitchWebsocketClient.setDataBundleListener(TwitchWebsocketDataBundleHandler(
                channelPointRedemptionHandler = TwitchChannelPointRedemptionHandler(
                    casualGamePollRedemption = self.__casualGamePollPointRedemption,
                    cutenessRedemption = self.__cutenessPointRedemption,
                    pkmnBattleRedemption = self.__pkmnBattlePointRedemption,
                    pkmnCatchRedemption = self.__pkmnCatchPointRedemption,
                    pkmnEvolveRedemption = self.__pkmnEvolvePointRedemption,
                    pkmnShinyRedemption = self.__pkmnShinyPointRedemption,
                    superTriviaGameRedemption = self.__superTriviaGamePointRedemption,
                    triviaGameRedemption = self.__triviaGamePointRedemption,
                    timber = self.__timber,
                    twitchChannelProvider = self,
                    userIdsRepository = self.__userIdsRepository
                ),
                cheerHandler = cheerHandler,
                pollHandler = pollHandler,
                predictionHandler = predictionHandler,
                raidHandler = raidHandler,
                subscriptionHandler = subscriptionHandler,
                timber = self.__timber,
                userIdsRepository = self.__userIdsRepository,
                usersRepository = self.__usersRepository
            ))

            self.__twitchWebsocketClient.start()

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBot', f'Joining channels: {event.getChannels()}')
        await self.join_channels(event.getChannels())

    async def onNewRecurringActionEvent(self, event: RecurringEvent):
        await self.wait_for_ready()

        self.__timber.log('CynanBot', f'Received new recurring action event: \"{event}\"')
        eventType = event.getEventType()

        if eventType is RecurringEventType.SUPER_TRIVIA:
            await self.__handleSuperTriviaRecurringActionEvent(event)
        elif eventType is RecurringEventType.WEATHER:
            await self.__handleWeatherRecurringActionEvent(event)
        elif eventType is RecurringEventType.WORD_OF_THE_DAY:
            await self.__handleWordOfTheDayRecurringActionEvent(event)

    async def __handleSuperTriviaRecurringActionEvent(self, event: SuperTriviaRecurringEvent):
        assert isinstance(event, SuperTriviaRecurringEvent), f"malformed {event=}"

        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, 'Super trivia starting soon!')

    async def __handleWeatherRecurringActionEvent(self, event: WeatherRecurringEvent):
        assert isinstance(event, WeatherRecurringEvent), f"malformed {event=}"

        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, event.getWeatherReport().toStr())

    async def __handleWordOfTheDayRecurringActionEvent(self, event: WordOfTheDayRecurringEvent):
        assert isinstance(event, WordOfTheDayRecurringEvent), f"malformed {event=}"

        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, event.getWordOfTheDayResponse().toStr())

    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        await self.wait_for_ready()

        self.__timber.log('CynanBot', f'Received new trivia event: \"{event}\"')
        eventType = event.getTriviaEventType()

        if eventType is TriviaEventType.CLEARED_SUPER_TRIVIA_QUEUE:
            await self.__handleClearedSuperTriviaQueueTriviaEvent(event)
        elif eventType is TriviaEventType.CORRECT_ANSWER:
            await self.__handleCorrectAnswerTriviaEvent(event)
        elif eventType is TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionTriviaEvent(event)
        elif eventType is TriviaEventType.GAME_OUT_OF_TIME:
            await self.__handleGameOutOfTimeTriviaEvent(event)
        elif eventType is TriviaEventType.INCORRECT_ANSWER:
            await self.__handleIncorrectAnswerTriviaEvent(event)
        elif eventType is TriviaEventType.INVALID_ANSWER_INPUT:
            await self.__handleInvalidAnswerInputTriviaEvent(event)
        elif eventType is TriviaEventType.NEW_GAME:
            await self.__handleNewTriviaGameEvent(event)
        elif eventType is TriviaEventType.NEW_SUPER_GAME:
            await self.__handleNewSuperTriviaGameEvent(event)
        elif eventType is TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION:
            await self.__handleFailedToFetchQuestionSuperTriviaEvent(event)
        elif eventType is TriviaEventType.SUPER_GAME_CORRECT_ANSWER:
            await self.__handleSuperGameCorrectAnswerTriviaEvent(event)
        elif eventType is TriviaEventType.SUPER_GAME_OUT_OF_TIME:
            await self.__handleSuperGameOutOfTimeTriviaEvent(event)

    async def __handleClearedSuperTriviaQueueTriviaEvent(self, event: ClearedSuperTriviaQueueTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getClearedSuperTriviaQueueMessage(
            numberOfGamesRemoved = event.getNumberOfGamesRemoved()
        ))

    async def __handleCorrectAnswerTriviaEvent(self, event: CorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        twitchUser = await self.__usersRepository.getUserAsync(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            newCuteness = event.getCutenessResult(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            twitchUser = twitchUser,
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleFailedToFetchQuestionTriviaEvent(self, event: FailedToFetchQuestionTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch trivia question')

    async def __handleFailedToFetchQuestionSuperTriviaEvent(self, event: FailedToFetchQuestionSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        await self.__twitchUtils.safeSend(twitchChannel, f'⚠ Unable to fetch super trivia question')

    async def __handleGameOutOfTimeTriviaEvent(self, event: OutOfTimeTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleIncorrectAnswerTriviaEvent(self, event: IncorrectAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getIncorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleInvalidAnswerInputTriviaEvent(self, event: InvalidAnswerInputTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getInvalidAnswerInputPrompt(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleNewTriviaGameEvent(self, event: NewTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        twitchUser = await self.__usersRepository.getUserAsync(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            emote = event.getEmote(),
            userNameThatRedeemed = event.getUserName(),
            twitchUser = twitchUser,
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleNewSuperTriviaGameEvent(self, event: NewSuperTriviaGameEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        twitchUser = await self.__usersRepository.getUserAsync(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaGameQuestionPrompt(
            triviaQuestion = event.getTriviaQuestion(),
            delaySeconds = event.getSecondsToLive(),
            points = event.getPointsForWinning(),
            emote = event.getEmote(),
            twitchUser = twitchUser,
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

    async def __handleSuperGameCorrectAnswerTriviaEvent(self, event: CorrectSuperAnswerTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        twitchUser = await self.__usersRepository.getUserAsync(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaCorrectAnswerReveal(
            question = event.getTriviaQuestion(),
            newCuteness = event.getCutenessResult(),
            points = event.getPointsForWinning(),
            emote = event.getEmote(),
            userName = event.getUserName(),
            twitchUser = twitchUser,
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.getToxicTriviaPunishmentResult(),
            emote = event.getEmote(),
            twitchUser = twitchUser
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.getRemainingQueueSize()
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    async def __handleSuperGameOutOfTimeTriviaEvent(self, event: OutOfTimeSuperTriviaEvent):
        twitchChannel = await self.__getChannel(event.getTwitchChannel())
        twitchUser = await self.__usersRepository.getUserAsync(event.getTwitchChannel())

        await self.__twitchUtils.safeSend(twitchChannel, await self.__triviaUtils.getSuperTriviaOutOfTimeAnswerReveal(
            question = event.getTriviaQuestion(),
            emote = event.getEmote(),
            specialTriviaStatus = event.getSpecialTriviaStatus()
        ))

        toxicTriviaPunishmentPrompt = await self.__triviaUtils.getToxicTriviaPunishmentMessage(
            toxicTriviaPunishmentResult = event.getToxicTriviaPunishmentResult(),
            emote = event.getEmote(),
            twitchUser = twitchUser
        )

        if utils.isValidStr(toxicTriviaPunishmentPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, toxicTriviaPunishmentPrompt)

        launchpadPrompt = await self.__triviaUtils.getSuperTriviaLaunchpadPrompt(
            remainingQueueSize = event.getRemainingQueueSize()
        )

        if utils.isValidStr(launchpadPrompt):
            await self.__twitchUtils.safeSend(twitchChannel, launchpadPrompt)

    @commands.command(name = 'addbannedtriviacontroller')
    async def command_addbannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addBannedTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'addcheeraction')
    async def command_addcheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addglobaltriviacontroller')
    async def command_addglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGlobalTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'addtriviaanswer')
    async def command_addtriviaanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaAnswerCommand.handleCommand(context)

    @commands.command(name = 'addtriviacontroller')
    async def command_addtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'adduser')
    async def command_adduser(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addUserCommand.handleCommand(context)

    @commands.command(name = 'answer', aliases = [ 'ANSWER', 'Answer', 'a', 'A' ])
    async def command_answer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__answerCommand.handleCommand(context)

    @commands.command(name = 'bantriviaquestion', aliases = [ 'bantrivia' ])
    async def command_bantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__banTriviaQuestionCommand.handleCommand(context)

    @commands.command(name = 'clearcaches')
    async def command_clearcaches(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearCachesCommand.handleCommand(context)

    @commands.command(name = 'clearsupertriviaqueue')
    async def command_clearsupertriviaqueue(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearSuperTriviaQueueCommand.handleCommand(context)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__commandsCommand.handleCommand(context)

    @commands.command(name = 'confirm')
    async def command_confirm(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__confirmCommand.handleCommand(context)

    @commands.command(name = 'cuteness', aliases = [ 'CUTENESS' ])
    async def command_cuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessCommand.handleCommand(context)

    @commands.command(name = 'cutenesschampions')
    async def command_cutenesschampions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessChampionsCommand.handleCommand(context)

    @commands.command(name = 'cutenesshistory')
    async def command_cutenesshistory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessHistoryCommand.handleCommand(context)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cynanSourceCommand.handleCommand(context)

    @commands.command(name = 'deletecheeraction')
    async def command_deletecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteCheerActionCommand.handleCommand(context)

    @commands.command(name = 'deletetriviaanswers')
    async def command_deletetriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteTriviaAnswersCommand.handleCommand(context)

    @commands.command(name = 'discord')
    async def command_discord(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__discordCommand.handleCommand(context)

    @commands.command(name = 'getbannedtriviacontrollers')
    async def command_getbannedtriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getBannedTriviaControllersCommand.handleCommand(context)

    @commands.command(name = 'getcheeractions')
    async def command_getcheeractions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getCheerActionsCommand.handleCommand(context)

    @commands.command(name = 'getglobaltriviacontrollers')
    async def command_getglobaltriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getGlobalTriviaControllersCommand.handleCommand(context)

    @commands.command(name = 'gettriviaanswers')
    async def command_gettriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaAnswersCommand.handleCommand(context)

    @commands.command(name = 'gettriviacontrollers')
    async def command_gettriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaControllersCommand.handleCommand(context)

    @commands.command(name = 'givecuteness')
    async def command_givecuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__giveCutenessCommand.handleCommand(context)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__jishoCommand.handleCommand(context)

    @commands.command(name = 'lorem')
    async def command_lorem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__loremIpsumCommand.handleCommand(context)

    @commands.command(name = 'mastodon')
    async def command_mastodon(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__mastodonCommand.handleCommand(context)

    @commands.command(name = 'mycutenesshistory', aliases = [ 'mycuteness' ])
    async def command_mycutenesshistory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__myCutenessHistoryCommand.handleCommand(context)

    @commands.command(name = 'pbs')
    async def command_pbs(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pbsCommand.handleCommand(context)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMonCommand.handleCommand(context)

    @commands.command(name = 'pkmove')
    async def command_pkmove(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMoveCommand.handleCommand(context)

    @commands.command(name = 'race')
    async def command_race(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__raceCommand.handleCommand(context)

    @commands.command(name = 'recurringaction')
    async def command_recurringaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__recurringActionCommand.handleCommand(context)

    @commands.command(name = 'recurringactions')
    async def command_recurringactions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__recurringActionsCommand.handleCommand(context)

    @commands.command(name = 'removebannedtriviacontroller')
    async def command_removebannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeBannedTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'removeglobaltriviacontroller')
    async def command_removeglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeGlobalTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'removetriviacontroller')
    async def command_removetriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeTriviaControllerCommand.handleCommand(context)

    @commands.command(name = 'setfuntoontoken')
    async def command_setfuntoontoken(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setFuntoonTokenCommand.handleCommand(context)

    @commands.command(name = 'settwitchcode')
    async def command_settwitchcode(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setTwitchCodeCommand.handleCommand(context)

    @commands.command(name = 'superanswer', aliases = [ 'SUPERANSWER', 'SuperAnswer', 'Superanswer', 'sa', 'SA', 'sanswer', 'SANSWER' ])
    async def command_superanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superAnswerCommand.handleChatCommand(context)

    @commands.command(name = 'supertrivia')
    async def command_supertrivia(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superTriviaCommand.handleCommand(context)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__swQuoteCommand.handleCommand(context)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__timeCommand.handleCommand(context)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__translateCommand.handleCommand(context)

    @commands.command(name = 'triviainfo')
    async def command_triviainfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaInfoCommand.handleCommand(context)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaScoreCommand.handleCommand(context)

    @commands.command(name = 'tts', aliases = [ 'TTS' ])
    async def command_tts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__ttsCommand.handleCommand(context)

    @commands.command(name = 'twitchinfo')
    async def command_twitchinfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__twitchInfoCommand.handleCommand(context)

    @commands.command(name = 'twitter')
    async def command_twitter(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__twitterCommand.handleCommand(context)

    @commands.command(name = 'unbantriviaquestion')
    async def command_unbantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__unbanTriviaQuestionCommand.handleCommand(context)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__weatherCommand.handleCommand(context)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__wordCommand.handleCommand(context)
