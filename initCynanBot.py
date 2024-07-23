import asyncio
import locale
from asyncio import AbstractEventLoop

from src.aniv.anivContentScanner import AnivContentScanner
from src.aniv.anivContentScannerInterface import AnivContentScannerInterface
from src.aniv.anivCopyMessageTimeoutScorePresenter import AnivCopyMessageTimeoutScorePresenter
from src.aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from src.aniv.anivCopyMessageTimeoutScoreRepository import AnivCopyMessageTimeoutScoreRepository
from src.aniv.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from src.aniv.anivSettingsRepository import AnivSettingsRepository
from src.aniv.anivSettingsRepositoryInterface import AnivSettingsRepositoryInterface
from src.aniv.anivUserIdProvider import AnivUserIdProvider
from src.aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from src.aniv.mostRecentAnivMessageRepository import MostRecentAnivMessageRepository
from src.aniv.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from src.aniv.mostRecentAnivMessageTimeoutHelper import MostRecentAnivMessageTimeoutHelper
from src.aniv.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from src.chatActions.anivCheckChatAction import AnivCheckChatAction
from src.chatActions.catJamChatAction import CatJamChatAction
from src.chatActions.chatActionsManager import ChatActionsManager
from src.chatActions.chatActionsManagerInterface import ChatActionsManagerInterface
from src.chatActions.chatLoggerChatAction import ChatLoggerChatAction
from src.chatActions.cheerActionsWizardChatAction import CheerActionsWizardChatAction
from src.chatActions.deerForceChatAction import DeerForceChatAction
from src.chatActions.persistAllUsersChatAction import PersistAllUsersChatAction
from src.chatActions.recurringActionsWizardChatAction import RecurringActionsWizardChatAction
from src.chatActions.saveMostRecentAnivMessageChatAction import SaveMostRecentAnivMessageChatAction
from src.chatActions.schubertWalkChatAction import SchubertWalkChatAction
from src.chatLogger.chatLogger import ChatLogger
from src.chatLogger.chatLoggerInterface import ChatLoggerInterface
from src.cheerActions.beanChance.beanChanceCheerActionHelper import BeanChanceCheerActionHelper
from src.cheerActions.beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from src.cheerActions.cheerActionHelper import CheerActionHelper
from src.cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from src.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from src.cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from src.cheerActions.cheerActionSettingsRepository import CheerActionSettingsRepository
from src.cheerActions.cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
from src.cheerActions.cheerActionsRepository import CheerActionsRepository
from src.cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from src.cheerActions.cheerActionsWizard import CheerActionsWizard
from src.cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from src.cheerActions.soundAlert.soundAlertCheerActionHelper import SoundAlertCheerActionHelper
from src.cheerActions.soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from src.cheerActions.timeout.timeoutCheerActionHelper import TimeoutCheerActionHelper
from src.cheerActions.timeout.timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from src.cheerActions.timeout.timeoutCheerActionHistoryRepository import TimeoutCheerActionHistoryRepository
from src.cheerActions.timeout.timeoutCheerActionHistoryRepositoryInterface import \
    TimeoutCheerActionHistoryRepositoryInterface
from src.cheerActions.timeout.timeoutCheerActionJsonMapper import TimeoutCheerActionJsonMapper
from src.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import TimeoutCheerActionJsonMapperInterface
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.cuteness.cutenessPresenter import CutenessPresenter
from src.cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from src.cuteness.cutenessRepository import CutenessRepository
from src.cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from src.cuteness.cutenessUtils import CutenessUtils
from src.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from src.cynanBot import CynanBot
from src.deepL.deepLApiService import DeepLApiService
from src.deepL.deepLApiServiceInterface import DeepLApiServiceInterface
from src.deepL.deepLJsonMapper import DeepLJsonMapper
from src.deepL.deepLJsonMapperInterface import DeepLJsonMapperInterface
from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.funtoon.funtoonJsonMapper import FuntoonJsonMapper
from src.funtoon.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from src.funtoon.funtoonRepository import FuntoonRepository
from src.funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from src.funtoon.funtoonTokensRepository import FuntoonTokensRepository
from src.funtoon.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from src.funtoon.funtoonUserIdProvider import FuntoonUserIdProvider
from src.funtoon.funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface
from src.google.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from src.google.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from src.google.googleApiService import GoogleApiService
from src.google.googleApiServiceInterface import GoogleApiServiceInterface
from src.google.googleJsonMapper import GoogleJsonMapper
from src.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.googleJwtBuilder import GoogleJwtBuilder
from src.google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from src.jisho.jishoApiService import JishoApiService
from src.jisho.jishoApiServiceInterface import JishoApiServiceInterface
from src.jisho.jishoJsonMapper import JishoJsonMapper
from src.jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from src.jisho.jishoPresenter import JishoPresenter
from src.jisho.jishoPresenterInterface import JishoPresenterInterface
from src.language.jishoHelper import JishoHelper
from src.language.jishoHelperInterface import JishoHelperInterface
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.language.translation.deepLTranslationApi import DeepLTranslationApi
from src.language.translation.googleTranslationApi import GoogleTranslationApi
from src.language.translationHelper import TranslationHelper
from src.language.translationHelperInterface import TranslationHelperInterface
from src.language.wordOfTheDayPresenter import WordOfTheDayPresenter
from src.language.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from src.language.wordOfTheDayRepository import WordOfTheDayRepository
from src.language.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from src.location.locationsRepository import LocationsRepository
from src.location.locationsRepositoryInterface import LocationsRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.administratorProvider import AdministratorProvider
from src.misc.administratorProviderInterface import AdministratorProviderInterface
from src.misc.authRepository import AuthRepository
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.misc.cynanBotUserIdsProvider import CynanBotUserIdsProvider
from src.misc.cynanBotUserIdsProviderInterface import CynanBotUserIdsProviderInterface
from src.misc.generalSettingsRepository import GeneralSettingsRepository
from src.mostRecentChat.mostRecentChatsRepository import MostRecentChatsRepository
from src.mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from src.network.aioHttpClientProvider import AioHttpClientProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.network.networkClientType import NetworkClientType
from src.network.networkJsonMapper import NetworkJsonMapper
from src.network.networkJsonMapperInterface import NetworkJsonMapperInterface
from src.network.requestsClientProvider import RequestsClientProvider
from src.nightbot.nightbotUserIdProvider import NightbotUserIdProvider
from src.nightbot.nightbotUserIdProviderInterface import NightbotUserIdProviderInterface
from src.openWeather.openWeatherApiService import OpenWeatherApiService
from src.openWeather.openWeatherApiServiceInterface import OpenWeatherApiServiceInterface
from src.openWeather.openWeatherJsonMapper import OpenWeatherJsonMapper
from src.openWeather.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from src.pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from src.pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from src.pkmn.pokepediaRepository import PokepediaRepository
from src.pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from src.recurringActions.mostRecentRecurringActionRepository import MostRecentRecurringActionRepository
from src.recurringActions.mostRecentRecurringActionRepositoryInterface import \
    MostRecentRecurringActionRepositoryInterface
from src.recurringActions.recurringActionsHelper import RecurringActionsHelper
from src.recurringActions.recurringActionsHelperInterface import RecurringActionsHelperInterface
from src.recurringActions.recurringActionsJsonParser import RecurringActionsJsonParser
from src.recurringActions.recurringActionsJsonParserInterface import RecurringActionsJsonParserInterface
from src.recurringActions.recurringActionsMachine import RecurringActionsMachine
from src.recurringActions.recurringActionsMachineInterface import RecurringActionsMachineInterface
from src.recurringActions.recurringActionsRepository import RecurringActionsRepository
from src.recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from src.recurringActions.recurringActionsWizard import RecurringActionsWizard
from src.recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from src.sentMessageLogger.sentMessageLogger import SentMessageLogger
from src.sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from src.soundPlayerManager.immediateSoundPlayerManager import ImmediateSoundPlayerManager
from src.soundPlayerManager.immediateSoundPlayerManagerInterface import ImmediateSoundPlayerManagerInterface
from src.soundPlayerManager.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from src.soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from src.soundPlayerManager.soundPlayerRandomizerHelper import SoundPlayerRandomizerHelper
from src.soundPlayerManager.soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface
from src.soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from src.soundPlayerManager.vlc.vlcSoundPlayerManagerProvider import VlcSoundPlayerManagerProvider
from src.starWars.starWarsQuotesRepository import StarWarsQuotesRepository
from src.starWars.starWarsQuotesRepositoryInterface import StarWarsQuotesRepositoryInterface
from src.storage.backingDatabase import BackingDatabase
from src.storage.backingPsqlDatabase import BackingPsqlDatabase
from src.storage.backingSqliteDatabase import BackingSqliteDatabase
from src.storage.databaseType import DatabaseType
from src.storage.jsonFileReader import JsonFileReader
from src.storage.linesFileReader import LinesFileReader
from src.storage.psqlCredentialsProvider import PsqlCredentialsProvider
from src.storage.storageJsonMapper import StorageJsonMapper
from src.storage.storageJsonMapperInterface import StorageJsonMapperInterface
from src.streamAlertsManager.streamAlertsManager import StreamAlertsManager
from src.streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from src.streamAlertsManager.streamAlertsSettingsRepository import StreamAlertsSettingsRepository
from src.streamAlertsManager.streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface
from src.streamElements.streamElementsUserIdProvider import StreamElementsUserIdProvider
from src.streamElements.streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface
from src.streamLabs.streamLabsUserIdProvider import StreamLabsUserIdProvider
from src.streamLabs.streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface
from src.supStreamer.supStreamerRepository import SupStreamerRepository
from src.supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from src.systemCommandHelper.systemCommandHelper import SystemCommandHelper
from src.systemCommandHelper.systemCommandHelperInterface import SystemCommandHelperInterface
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface
from src.transparent.transparentApiService import TransparentApiService
from src.transparent.transparentApiServiceInterface import TransparentApiServiceInterface
from src.transparent.transparentXmlMapper import TransparentXmlMapper
from src.transparent.transparentXmlMapperInterface import TransparentXmlMapperInterface
from src.trivia.additionalAnswers.additionalTriviaAnswersRepository import AdditionalTriviaAnswersRepository
from src.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from src.trivia.banned.bannedTriviaGameControllersRepository import BannedTriviaGameControllersRepository
from src.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from src.trivia.banned.bannedTriviaIdsRepository import BannedTriviaIdsRepository
from src.trivia.banned.bannedTriviaIdsRepositoryInterface import BannedTriviaIdsRepositoryInterface
from src.trivia.banned.triviaBanHelper import TriviaBanHelper
from src.trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from src.trivia.builder.triviaGameBuilder import TriviaGameBuilder
from src.trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from src.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from src.trivia.compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from src.trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from src.trivia.content.triviaContentScanner import TriviaContentScanner
from src.trivia.content.triviaContentScannerInterface import TriviaContentScannerInterface
from src.trivia.emotes.triviaEmoteGenerator import TriviaEmoteGenerator
from src.trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from src.trivia.emotes.triviaEmoteRepository import TriviaEmoteRepository
from src.trivia.emotes.triviaEmoteRepositoryInterface import TriviaEmoteRepositoryInterface
from src.trivia.gameController.triviaGameControllersRepository import TriviaGameControllersRepository
from src.trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from src.trivia.gameController.triviaGameGlobalControllersRepository import TriviaGameGlobalControllersRepository
from src.trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from src.trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from src.trivia.games.triviaGameStore import TriviaGameStore
from src.trivia.score.triviaScoreRepository import TriviaScoreRepository
from src.trivia.score.triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from src.trivia.scraper.triviaScraper import TriviaScraper
from src.trivia.scraper.triviaScraperInterface import TriviaScraperInterface
from src.trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from src.trivia.specialStatus.shinyTriviaOccurencesRepository import ShinyTriviaOccurencesRepository
from src.trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from src.trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from src.trivia.specialStatus.toxicTriviaOccurencesRepository import ToxicTriviaOccurencesRepository
from src.trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from src.trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from src.trivia.triviaAnswerChecker import TriviaAnswerChecker
from src.trivia.triviaGameMachine import TriviaGameMachine
from src.trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from src.trivia.triviaHistoryRepository import TriviaHistoryRepository
from src.trivia.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from src.trivia.triviaIdGenerator import TriviaIdGenerator
from src.trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from src.trivia.triviaQuestionPresenter import TriviaQuestionPresenter
from src.trivia.triviaQuestionPresenterInterface import TriviaQuestionPresenterInterface
from src.trivia.triviaRepositories.bongoTriviaQuestionRepository import BongoTriviaQuestionRepository
from src.trivia.triviaRepositories.funtoonTriviaQuestionRepository import FuntoonTriviaQuestionRepository
from src.trivia.triviaRepositories.glacialTriviaQuestionRepository import GlacialTriviaQuestionRepository
from src.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from src.trivia.triviaRepositories.jServiceTriviaQuestionRepository import JServiceTriviaQuestionRepository
from src.trivia.triviaRepositories.lotrTriviaQuestionsRepository import LotrTriviaQuestionRepository
from src.trivia.triviaRepositories.millionaireTriviaQuestionRepository import MillionaireTriviaQuestionRepository
from src.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from src.trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import OpenTriviaQaTriviaQuestionRepository
from src.trivia.triviaRepositories.pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from src.trivia.triviaRepositories.quizApiTriviaQuestionRepository import QuizApiTriviaQuestionRepository
from src.trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import TriviaDatabaseTriviaQuestionRepository
from src.trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from src.trivia.triviaRepositories.triviaRepository import TriviaRepository
from src.trivia.triviaRepositories.triviaRepositoryInterface import TriviaRepositoryInterface
from src.trivia.triviaRepositories.willFryTriviaQuestionRepository import WillFryTriviaQuestionRepository
from src.trivia.triviaRepositories.wwtbamTriviaQuestionRepository import WwtbamTriviaQuestionRepository
from src.trivia.triviaSettingsRepository import TriviaSettingsRepository
from src.trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from src.trivia.triviaSourceInstabilityHelper import TriviaSourceInstabilityHelper
from src.trivia.triviaUtils import TriviaUtils
from src.trivia.triviaUtilsInterface import TriviaUtilsInterface
from src.trivia.triviaVerifier import TriviaVerifier
from src.trivia.triviaVerifierInterface import TriviaVerifierInterface
from src.tts.decTalk.decTalkFileManager import DecTalkFileManager
from src.tts.decTalk.decTalkFileManagerInterface import DecTalkFileManagerInterface
from src.tts.decTalk.decTalkManager import DecTalkManager
from src.tts.decTalk.decTalkVoiceChooser import DecTalkVoiceChooser
from src.tts.decTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from src.tts.decTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from src.tts.decTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.tts.google.googleFileExtensionHelper import GoogleFileExtensionHelper
from src.tts.google.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from src.tts.google.googleTtsFileManager import GoogleTtsFileManager
from src.tts.google.googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from src.tts.google.googleTtsManager import GoogleTtsManager
from src.tts.google.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from src.tts.google.googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from src.tts.tempFileHelper.ttsTempFileHelper import TtsTempFileHelper
from src.tts.tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from src.tts.ttsCommandBuilder import TtsCommandBuilder
from src.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from src.tts.ttsJsonMapper import TtsJsonMapper
from src.tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.ttsManager import TtsManager
from src.tts.ttsManagerInterface import TtsManagerInterface
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from src.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from src.twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from src.twitch.api.twitchApiService import TwitchApiService
from src.twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.configuration.twitchChannelJoinHelper import TwitchChannelJoinHelper
from src.twitch.configuration.twitchCheerHandler import TwitchCheerHandler
from src.twitch.configuration.twitchConfiguration import TwitchConfiguration
from src.twitch.configuration.twitchIo.twitchIoConfiguration import TwitchIoConfiguration
from src.twitch.configuration.twitchRaidHandler import TwitchRaidHandler
from src.twitch.emotes.twitchEmotesHelper import TwitchEmotesHelper
from src.twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from src.twitch.followingStatus.twitchFollowingStatusRepository import TwitchFollowingStatusRepository
from src.twitch.followingStatus.twitchFollowingStatusRepositoryInterface import \
    TwitchFollowingStatusRepositoryInterface
from src.twitch.isLiveOnTwitchRepository import IsLiveOnTwitchRepository
from src.twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from src.twitch.timeout.timeoutImmuneUserIdsRepository import TimeoutImmuneUserIdsRepository
from src.twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from src.twitch.timeout.twitchTimeoutHelper import TwitchTimeoutHelper
from src.twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from src.twitch.timeout.twitchTimeoutRemodHelper import TwitchTimeoutRemodHelper
from src.twitch.timeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from src.twitch.timeout.twitchTimeoutRemodRepository import TwitchTimeoutRemodRepository
from src.twitch.timeout.twitchTimeoutRemodRepositoryInterface import TwitchTimeoutRemodRepositoryInterface
from src.twitch.twitchAnonymousUserIdProvider import TwitchAnonymousUserIdProvider
from src.twitch.twitchAnonymousUserIdProviderInterface import TwitchAnonymousUserIdProviderInterface
from src.twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from src.twitch.twitchPredictionWebsocketUtils import TwitchPredictionWebsocketUtils
from src.twitch.twitchTokensRepository import TwitchTokensRepository
from src.twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from src.twitch.twitchTokensUtils import TwitchTokensUtils
from src.twitch.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from src.twitch.twitchUtils import TwitchUtils
from src.twitch.twitchUtilsInterface import TwitchUtilsInterface
from src.twitch.websocket.twitchWebsocketAllowedUsersRepository import TwitchWebsocketAllowedUsersRepository
from src.twitch.websocket.twitchWebsocketClient import TwitchWebsocketClient
from src.twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from src.users.modifyUserDataHelper import ModifyUserDataHelper
from src.users.userIdsRepository import UserIdsRepository
from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from src.users.usersRepository import UsersRepository
from src.users.usersRepositoryInterface import UsersRepositoryInterface
from src.weather.weatherReportPresenter import WeatherReportPresenter
from src.weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from src.weather.weatherRepository import WeatherRepository
from src.weather.weatherRepositoryInterface import WeatherRepositoryInterface

# Uncomment this chunk to turn on extra extra debug logging
# logging.basicConfig(
#     filename = 'generalLogging.log',
#     level = logging.DEBUG
# )


locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Core initialization section ##
#################################

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper,
    timeZoneRepository = timeZoneRepository
)

networkJsonMapper: NetworkJsonMapperInterface = NetworkJsonMapper()
storageJsonMapper: StorageJsonMapperInterface = StorageJsonMapper()

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonFileReader('generalSettingsRepository.json'),
    networkJsonMapper = networkJsonMapper,
    storageJsonMapper = storageJsonMapper
)

generalSettingsSnapshot = generalSettingsRepository.getAll()

backingDatabase: BackingDatabase
match generalSettingsSnapshot.requireDatabaseType():
    case DatabaseType.POSTGRESQL:
        backingDatabase = BackingPsqlDatabase(
            eventLoop = eventLoop,
            psqlCredentialsProvider = PsqlCredentialsProvider(
                credentialsJsonReader = JsonFileReader('psqlCredentials.json')
            ),
            timber = timber
        )

    case DatabaseType.SQLITE:
        backingDatabase = BackingSqliteDatabase(
            eventLoop = eventLoop
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured DatabaseType: \"{generalSettingsSnapshot.requireDatabaseType()}\"')

networkClientProvider: NetworkClientProvider
match generalSettingsSnapshot.requireNetworkClientType():
    case NetworkClientType.AIOHTTP:
        networkClientProvider = AioHttpClientProvider(
            eventLoop = eventLoop,
            timber = timber
        )

    case NetworkClientType.REQUESTS:
        networkClientProvider = RequestsClientProvider(
            timber = timber
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured NetworkClientType: \"{generalSettingsSnapshot.requireNetworkClientType()}\"')

authRepository = AuthRepository(
    authJsonReader = JsonFileReader('authRepository.json')
)

twitchJsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
    timber = timber,
    twitchJsonMapper = twitchJsonMapper
)

twitchApiService: TwitchApiServiceInterface = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchCredentialsProvider = authRepository,
    twitchJsonMapper = twitchJsonMapper,
    twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
)

twitchAnonymousUserIdProvider: TwitchAnonymousUserIdProviderInterface = TwitchAnonymousUserIdProvider()

userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchAnonymousUserIdProvider = twitchAnonymousUserIdProvider,
    twitchApiService = twitchApiService
)

twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('twitchTokensRepositorySeedFile.json')
)

administratorProvider: AdministratorProviderInterface = AdministratorProvider(
    generalSettingsRepository = generalSettingsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader('bannedWords.txt'),
    timber = timber
)

contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber
)

twitchTokensUtils: TwitchTokensUtilsInterface = TwitchTokensUtils(
    administratorProvider = administratorProvider,
    twitchTokensRepository = twitchTokensRepository
)

twitchEmotesHelper: TwitchEmotesHelperInterface = TwitchEmotesHelper(
    timber = timber,
    twitchApiService = twitchApiService
)

twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = TwitchFollowingStatusRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository
)

soundAlertJsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper(
    timber = timber
)

usersRepository: UsersRepositoryInterface = UsersRepository(
    soundAlertJsonMapper = soundAlertJsonMapper,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchChannelJoinHelper: TwitchChannelJoinHelperInterface = TwitchChannelJoinHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    verified = True,
    timber = timber,
    usersRepository = usersRepository
)

modifyUserDataHelper: ModifyUserDataHelper = ModifyUserDataHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

chatLogger: ChatLoggerInterface = ChatLogger(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface = CynanBotUserIdsProvider()


#####################################
## Cuteness initialization section ##
#####################################

cutenessPresenter: CutenessPresenterInterface = CutenessPresenter()

cutenessRepository: CutenessRepositoryInterface = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)

cutenessUtils: CutenessUtilsInterface = CutenessUtils()


#####################################
## Nightbot initialization section ##
#####################################

nightbotUserIdProvider: NightbotUserIdProviderInterface = NightbotUserIdProvider()


####################################
## Funtoon initialization section ##
####################################

funtoonUserIdProvider: FuntoonUserIdProviderInterface = FuntoonUserIdProvider()

funtoonTokensRepository: FuntoonTokensRepositoryInterface = FuntoonTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('funtoonTokensRepositorySeedFile.json')
)

funtoonJsonMapper: FuntoonJsonMapperInterface = FuntoonJsonMapper()

funtoonRepository: FuntoonRepositoryInterface = FuntoonRepository(
    funtoonJsonMapper = funtoonJsonMapper,
    funtoonTokensRepository = funtoonTokensRepository,
    networkClientProvider = networkClientProvider,
    timber = timber
)

emojiRepository: EmojiRepositoryInterface = EmojiRepository(
    emojiJsonReader = JsonFileReader('emojiRepository.json'),
    timber = timber
)

emojiHelper: EmojiHelperInterface = EmojiHelper(
    emojiRepository = emojiRepository
)

isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = IsLiveOnTwitchRepository(
    administratorProvider = administratorProvider,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchTokensRepository = twitchTokensRepository
)

languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

locationsRepository: LocationsRepositoryInterface = LocationsRepository(
    locationsJsonReader = JsonFileReader('locationsRepository.json'),
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

mostRecentChatsRepository: MostRecentChatsRepositoryInterface = MostRecentChatsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

pokepediaJsonMapper: PokepediaJsonMapperInterface = PokepediaJsonMapper(
    timber = timber
)

pokepediaRepository: PokepediaRepositoryInterface = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    pokepediaJsonMapper = pokepediaJsonMapper,
    timber = timber
)

systemCommandHelper: SystemCommandHelperInterface = SystemCommandHelper(
    timber = timber
)

twitchConfiguration: TwitchConfiguration = TwitchIoConfiguration(
    userIdsRepository = userIdsRepository
)

sentMessageLogger: SentMessageLoggerInterface = SentMessageLogger(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface = TwitchTimeoutRemodRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface = TwitchTimeoutRemodHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchTimeoutRemodRepository = twitchTimeoutRemodRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

twitchUtils: TwitchUtilsInterface = TwitchUtils(
    backgroundTaskHelper = backgroundTaskHelper,
    generalSettingsRepository = generalSettingsRepository,
    sentMessageLogger = sentMessageLogger,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

streamElementsUserIdProvider: StreamElementsUserIdProviderInterface = StreamElementsUserIdProvider()

streamLabsUserIdProvider: StreamLabsUserIdProviderInterface = StreamLabsUserIdProvider()

timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface =  TimeoutImmuneUserIdsRepository(
    cynanBotUserIdsProvider = cynanBotUserIdsProvider,
    funtoonUserIdProvider = funtoonUserIdProvider,
    nightbotUserIdProvider = nightbotUserIdProvider,
    streamElementsUserIdProvider = streamElementsUserIdProvider,
    streamLabsUserIdProvider = streamLabsUserIdProvider,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository
)

twitchTimeoutHelper: TwitchTimeoutHelperInterface = TwitchTimeoutHelper(
    timber = timber,
    timeoutImmuneUserIdsRepository = timeoutImmuneUserIdsRepository,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchConstants = twitchUtils,
    twitchHandleProvider = authRepository,
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    userIdsRepository = userIdsRepository
)

transparentXmlMapper: TransparentXmlMapperInterface = TransparentXmlMapper(
    timeZoneRepository = timeZoneRepository
)

transparentApiService: TransparentApiServiceInterface = TransparentApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    transparentXmlMapper = transparentXmlMapper
)

wordOfTheDayRepository: WordOfTheDayRepositoryInterface = WordOfTheDayRepository(
    timber = timber,
    transparentApiService = transparentApiService
)

wordOfTheDayPresenter: WordOfTheDayPresenterInterface = WordOfTheDayPresenter()

deepLJsonMapper: DeepLJsonMapperInterface = DeepLJsonMapper(
    languagesRepository = languagesRepository,
    timber = timber
)

deepLApiService: DeepLApiServiceInterface = DeepLApiService(
    deepLAuthKeyProvider = authRepository,
    deepLJsonMapper = deepLJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber
)

deepLTranslationApi = DeepLTranslationApi(
    deepLApiService = deepLApiService,
    deepLAuthKeyProvider = authRepository,
    timber = timber
)

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

googleJwtBuilder: GoogleJwtBuilderInterface = GoogleJwtBuilder(
    googleCloudCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    timeZoneRepository = timeZoneRepository
)

googleApiService: GoogleApiServiceInterface = GoogleApiService(
    googleApiAccessTokenStorage = googleApiAccessTokenStorage,
    googleCloudProjectCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    googleJwtBuilder = googleJwtBuilder,
    networkClientProvider = networkClientProvider,
    timber = timber
)

googleTranslationApi = GoogleTranslationApi(
    googleApiService = googleApiService,
    googleCloudProjectCredentialsProvider = authRepository,
    languagesRepository = languagesRepository,
    timber = timber
)

translationHelper: TranslationHelperInterface | None = TranslationHelper(
    deepLTranslationApi = deepLTranslationApi,
    googleTranslationApi = googleTranslationApi,
    languagesRepository = languagesRepository,
    timber = timber
)

twitchWebsocketClient: TwitchWebsocketClientInterface | None = None
if generalSettingsSnapshot.isEventSubEnabled():
    twitchWebsocketClient = TwitchWebsocketClient(
        backgroundTaskHelper = backgroundTaskHelper,
        timber = timber,
        timeZoneRepository = timeZoneRepository,
        twitchApiService = twitchApiService,
        twitchTokensRepository = twitchTokensRepository,
        twitchWebsocketAllowedUsersRepository = TwitchWebsocketAllowedUsersRepository(
            timber = timber,
            twitchTokensRepository = twitchTokensRepository,
            userIdsRepository = userIdsRepository,
            usersRepository = usersRepository
        ),
        twitchWebsocketJsonMapper = twitchWebsocketJsonMapper
    )

authSnapshot = authRepository.getAll()

openWeatherJsonMapper: OpenWeatherJsonMapperInterface = OpenWeatherJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

openWeatherApiService: OpenWeatherApiServiceInterface = OpenWeatherApiService(
    networkClientProvider = networkClientProvider,
    openWeatherApiKeyProvider = authRepository,
    openWeatherJsonMapper = openWeatherJsonMapper,
    timber = timber
)

weatherReportPresenter: WeatherReportPresenterInterface = WeatherReportPresenter()

weatherRepository: WeatherRepositoryInterface = WeatherRepository(
    openWeatherApiKeyProvider = authRepository,
    openWeatherApiService = openWeatherApiService,
    timber = timber
)


###################################
## Trivia initialization section ##
###################################

shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository
)
toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = ToxicTriviaOccurencesRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository
)
triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)
triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
    timber = timber
)
triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()
triviaSourceInstabilityHelper: TriviaSourceInstabilityHelper = TriviaSourceInstabilityHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)
additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = AdditionalTriviaAnswersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
bannedTriviaIdsRepository: BannedTriviaIdsRepositoryInterface = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber
)
shinyTriviaHelper = ShinyTriviaHelper(
    cutenessRepository = cutenessRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaSettingsRepository = triviaSettingsRepository
)
toxicTriviaHelper = ToxicTriviaHelper(
    toxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    contentScanner = contentScanner,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaEmoteRepository: TriviaEmoteRepositoryInterface = TriviaEmoteRepository(
    backingDatabase = backingDatabase
)
triviaEmoteGenerator: TriviaEmoteGeneratorInterface = TriviaEmoteGenerator(
    timber = timber,
    triviaEmoteRepository = triviaEmoteRepository
)
triviaGameBuilder: TriviaGameBuilderInterface = TriviaGameBuilder(
    triviaGameBuilderSettings = generalSettingsRepository,
    triviaIdGenerator = triviaIdGenerator,
    usersRepository = usersRepository
)
bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = BannedTriviaGameControllersRepository(
    administratorProvider = administratorProvider,
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = TriviaGameControllersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface = TriviaGameGlobalControllersRepository(
    administratorProvider = administratorProvider,
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaHistoryRepository: TriviaHistoryRepositoryInterface = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaScoreRepository: TriviaScoreRepositoryInterface = TriviaScoreRepository(
    backingDatabase = backingDatabase
)

triviaQuestionPresenter: TriviaQuestionPresenterInterface = TriviaQuestionPresenter()

triviaUtils: TriviaUtilsInterface = TriviaUtils(
    administratorProvider = administratorProvider,
    bannedTriviaGameControllersRepository = bannedTriviaGameControllersRepository,
    timber = timber,
    triviaGameControllersRepository = triviaGameControllersRepository,
    triviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository,
    triviaQuestionPresenter = triviaQuestionPresenter,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)

quizApiTriviaQuestionRepository: QuizApiTriviaQuestionRepository | None = None
if authSnapshot.hasQuizApiKey():
    quizApiTriviaQuestionRepository = QuizApiTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        quizApiKey = authSnapshot.requireQuizApiKey(),
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
    backingDatabase = backingDatabase,
    networkClientProvider = networkClientProvider,
    timber = timber,
    triviaIdGenerator = triviaIdGenerator,
    triviaQuestionCompiler = triviaQuestionCompiler,
    triviaSettingsRepository = triviaSettingsRepository
)

glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface = GlacialTriviaQuestionRepository(
    additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaQuestionCompiler = triviaQuestionCompiler,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository
)

triviaBanHelper: TriviaBanHelperInterface = TriviaBanHelper(
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    funtoonRepository = funtoonRepository,
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    triviaSettingsRepository = triviaSettingsRepository
)

triviaVerifier: TriviaVerifierInterface = TriviaVerifier(
    timber = timber,
    triviaBanHelper = triviaBanHelper,
    triviaContentScanner = triviaContentScanner,
    triviaHistoryRepository = triviaHistoryRepository
)

triviaScraper: TriviaScraperInterface = TriviaScraper(
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)

triviaRepository: TriviaRepositoryInterface = TriviaRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    bongoTriviaQuestionRepository = BongoTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
        additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    glacialTriviaQuestionRepository = glacialTriviaQuestionRepository,
    jServiceTriviaQuestionRepository = JServiceTriviaQuestionRepository(
        additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    lotrTriviaQuestionRepository = LotrTriviaQuestionRepository(
        additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    millionaireTriviaQuestionRepository = MillionaireTriviaQuestionRepository(
        timber = timber,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    openTriviaDatabaseTriviaQuestionRepository = openTriviaDatabaseTriviaQuestionRepository,
    openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
        timber = timber,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
        pokepediaRepository = pokepediaRepository,
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    quizApiTriviaQuestionRepository = quizApiTriviaQuestionRepository,
    timber = timber,
    triviaDatabaseTriviaQuestionRepository = TriviaDatabaseTriviaQuestionRepository(
        timber = timber,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaQuestionCompanyTriviaQuestionRepository = TriviaQuestionCompanyTriviaQuestionRepository(
        timber = timber,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaScraper = triviaScraper,
    triviaSettingsRepository = triviaSettingsRepository,
    triviaSourceInstabilityHelper = triviaSourceInstabilityHelper,
    triviaVerifier = triviaVerifier,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository,
    willFryTriviaQuestionRepository = WillFryTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    wwtbamTriviaQuestionRepository = WwtbamTriviaQuestionRepository(
        timber = timber,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    )
)

triviaGameMachine: TriviaGameMachineInterface = TriviaGameMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    cutenessRepository = cutenessRepository,
    queuedTriviaGameStore = QueuedTriviaGameStore(
        timber = timber,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    shinyTriviaHelper = shinyTriviaHelper,
    superTriviaCooldownHelper = SuperTriviaCooldownHelper(
        timeZoneRepository = timeZoneRepository,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    toxicTriviaHelper = toxicTriviaHelper,
    triviaAnswerChecker = TriviaAnswerChecker(
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameStore = TriviaGameStore(),
    triviaIdGenerator = triviaIdGenerator,
    triviaRepository = triviaRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)


#################################
## Aniv initialization section ##
#################################

anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface = AnivCopyMessageTimeoutScorePresenter()

anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface = AnivCopyMessageTimeoutScoreRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository,
    userIdsRepository = userIdsRepository
)

anivSettingsRepository: AnivSettingsRepositoryInterface = AnivSettingsRepository(
    settingsJsonReader = JsonFileReader('anivSettingsRepository.json')
)

anivContentScanner: AnivContentScannerInterface = AnivContentScanner(
    contentScanner = contentScanner,
    timber = timber
)

anivUserIdProvider: AnivUserIdProviderInterface = AnivUserIdProvider()

mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None = MostRecentAnivMessageRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None = None
if mostRecentAnivMessageRepository is not None:
    mostRecentAnivMessageTimeoutHelper = MostRecentAnivMessageTimeoutHelper(
        anivCopyMessageTimeoutScoreRepository = anivCopyMessageTimeoutScoreRepository,
        anivSettingsRepository = anivSettingsRepository,
        anivUserIdProvider = anivUserIdProvider,
        mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
        timber = timber,
        timeZoneRepository = timeZoneRepository,
        twitchConstants = twitchUtils,
        twitchHandleProvider = authRepository,
        twitchTimeoutHelper = twitchTimeoutHelper,
        twitchTokensRepository = twitchTokensRepository,
        twitchUtils = twitchUtils
    )


##############################################
## Recurring Actions initialization section ##
##############################################

recurringActionsJsonParser: RecurringActionsJsonParserInterface = RecurringActionsJsonParser(
    languagesRepository = languagesRepository,
    timber = timber
)

recurringActionsRepository: RecurringActionsRepositoryInterface = RecurringActionsRepository(
    backingDatabase = backingDatabase,
    recurringActionsJsonParser = recurringActionsJsonParser,
    timber = timber
)

mostRecentRecurringActionRepository: MostRecentRecurringActionRepositoryInterface = MostRecentRecurringActionRepository(
    backingDatabase = backingDatabase,
    recurringActionsJsonParser = recurringActionsJsonParser,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

recurringActionsMachine: RecurringActionsMachineInterface = RecurringActionsMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    cutenessRepository = cutenessRepository,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    locationsRepository = locationsRepository,
    mostRecentRecurringActionRepository = mostRecentRecurringActionRepository,
    recurringActionsRepository = recurringActionsRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    triviaGameBuilder = triviaGameBuilder,
    triviaGameMachine = triviaGameMachine,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
)

recurringActionsHelper: RecurringActionsHelperInterface = RecurringActionsHelper(
    recurringActionsRepository = recurringActionsRepository,
    timber = timber
)

recurringActionsWizard: RecurringActionsWizardInterface = RecurringActionsWizard(
    timber = timber
)


#########################################
## Sound Player initialization section ##
#########################################

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonFileReader('soundPlayerSettingsRepository.json')
)

soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface | None = SoundPlayerRandomizerHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber
)

soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = VlcSoundPlayerManagerProvider(
    backgroundTaskHelper = backgroundTaskHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber
)

soundPlayerManager: SoundPlayerManagerInterface | None = soundPlayerManagerProvider.constructSoundPlayerManagerInstance()

immediateSoundPlayerManager: ImmediateSoundPlayerManagerInterface = ImmediateSoundPlayerManager(
    soundPlayerManagerProvider = soundPlayerManagerProvider,
    timber = timber
)


################################
## TTS initialization section ##
################################

ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
    timber = timber
)

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    googleJsonMapper = googleJsonMapper,
    settingsJsonReader = JsonFileReader('ttsSettingsRepository.json')
)

ttsCommandBuilder: TtsCommandBuilderInterface = TtsCommandBuilder(
    contentScanner = contentScanner,
    emojiHelper = emojiHelper,
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository
)

ttsTempFileHelper: TtsTempFileHelperInterface = TtsTempFileHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

decTalkFileManager: DecTalkFileManagerInterface = DecTalkFileManager(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber
)

decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

decTalkVoiceChooser: DecTalkVoiceChooserInterface = DecTalkVoiceChooser(
    decTalkVoiceMapper = decTalkVoiceMapper
)

decTalkManager: DecTalkManager | None = DecTalkManager(
    decTalkFileManager = decTalkFileManager,
    decTalkVoiceChooser = decTalkVoiceChooser,
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository,
    ttsTempFileHelper = ttsTempFileHelper
)

googleFileExtensionHelper: GoogleFileExtensionHelperInterface = GoogleFileExtensionHelper()

googleTtsFileManager: GoogleTtsFileManagerInterface = GoogleTtsFileManager(
    eventLoop = eventLoop,
    googleFileExtensionHelper = googleFileExtensionHelper,
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository
)

googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface = GoogleTtsVoiceChooser()

googleTtsManager: GoogleTtsManager | None = GoogleTtsManager(
    googleApiService = googleApiService,
    googleTtsFileManager = googleTtsFileManager,
    googleTtsVoiceChooser = googleTtsVoiceChooser,
    soundPlayerManager = soundPlayerManager,
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository,
    ttsTempFileHelper = ttsTempFileHelper
)

ttsManager: TtsManagerInterface | None = TtsManager(
    decTalkManager = decTalkManager,
    googleTtsManager = googleTtsManager,
    timber = timber,
    ttsMonsterManager = None,
    ttsSettingsRepository = ttsSettingsRepository,
    ttsTempFileHelper = ttsTempFileHelper
)


#################################################
## Stream Alerts Manager intialization section ##
#################################################

streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface = StreamAlertsSettingsRepository(
    settingsJsonReader = JsonFileReader('streamAlertsSettingsRepository.json')
)

streamAlertsManager: StreamAlertsManagerInterface | None = StreamAlertsManager(
    backgroundTaskHelper = backgroundTaskHelper,
    soundPlayerManager = soundPlayerManager,
    streamAlertsSettingsRepository = streamAlertsSettingsRepository,
    timber = timber,
    ttsManager = ttsManager
)


#############################################
## Star Wars Quotes initialization section ##
#############################################

starWarsQuotesRepository: StarWarsQuotesRepositoryInterface = StarWarsQuotesRepository(
    quotesJsonReader = JsonFileReader('starWarsQuotesRepository.json')
)


##################################
## Jisho initialization section ##
##################################

jishoJsonMapper: JishoJsonMapperInterface = JishoJsonMapper(
    timber = timber
)

jishoApiService: JishoApiServiceInterface = JishoApiService(
    jishoJsonMapper = jishoJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber
)

jishoPresenter: JishoPresenterInterface = JishoPresenter()

jishoHelper: JishoHelperInterface = JishoHelper(
    jishoApiService = jishoApiService,
    jishoPresenter = jishoPresenter,
    timber = timber
)


##########################################
## Cheer Actions initialization section ##
##########################################

cheerActionJsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
    timber = timber
)

cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface = CheerActionSettingsRepository(
    settingsJsonReader = JsonFileReader('cheerActionSettings.json')
)

cheerActionsRepository: CheerActionsRepositoryInterface = CheerActionsRepository(
    backingDatabase = backingDatabase,
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionSettingsRepository = cheerActionSettingsRepository,
    timber = timber
)

beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None = BeanChanceCheerActionHelper(
    timber = timber
)

soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None = SoundAlertCheerActionHelper(
    immediateSoundPlayerManager = immediateSoundPlayerManager,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
    timber = timber
)

timeoutCheerActionJsonMapper: TimeoutCheerActionJsonMapperInterface = TimeoutCheerActionJsonMapper(
    timber = timber
)

timeoutCheerActionHistoryRepository: TimeoutCheerActionHistoryRepositoryInterface = TimeoutCheerActionHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeoutCheerActionJsonMapper = timeoutCheerActionJsonMapper,
    timeZoneRepository = timeZoneRepository,
    userIdsRepository = userIdsRepository
)

timeoutCheerActionHelper: TimeoutCheerActionHelperInterface | None = TimeoutCheerActionHelper(
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    timeoutCheerActionHistoryRepository = timeoutCheerActionHistoryRepository,
    timeZoneRepository = timeZoneRepository,
    twitchFollowingStatusRepository = twitchFollowingStatusRepository,
    twitchTimeoutHelper = twitchTimeoutHelper,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository
)

cheerActionHelper: CheerActionHelperInterface = CheerActionHelper(
    beanChanceCheerActionHelper = beanChanceCheerActionHelper,
    cheerActionsRepository = cheerActionsRepository,
    soundAlertCheerActionHelper = soundAlertCheerActionHelper,
    timber = timber,
    timeoutCheerActionHelper = timeoutCheerActionHelper,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)


#########################################
## Chat Actions initialization section ##
#########################################

catJamChatAction = CatJamChatAction(
    generalSettingsRepository = generalSettingsRepository,
    timber = timber,
    twitchUtils = twitchUtils
)

chatLoggerChatAction = ChatLoggerChatAction(
    chatLogger = chatLogger
)

cheerActionsWizard: CheerActionsWizardInterface = CheerActionsWizard(
    timber = timber
)

cheerActionsWizardChatAction = CheerActionsWizardChatAction(
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionsRepository = cheerActionsRepository,
    cheerActionsWizard = cheerActionsWizard,
    timber = timber,
    twitchUtils = twitchUtils
)

persistAllUsersChatAction = PersistAllUsersChatAction(
    generalSettingsRepository = generalSettingsRepository,
    userIdsRepository = userIdsRepository
)

recurringActionsWizardChatAction = RecurringActionsWizardChatAction(
    recurringActionsRepository = recurringActionsRepository,
    recurringActionsWizard = recurringActionsWizard,
    timber = timber,
    twitchUtils = twitchUtils
)

saveMostRecentAnivMessageChatAction: SaveMostRecentAnivMessageChatAction | None = None
if mostRecentAnivMessageRepository is not None:
    saveMostRecentAnivMessageChatAction = SaveMostRecentAnivMessageChatAction(
        anivUserIdProvider = anivUserIdProvider,
        mostRecentAnivMessageRepository = mostRecentAnivMessageRepository
    )

supStreamerRepository: SupStreamerRepositoryInterface = SupStreamerRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

chatActionsManager: ChatActionsManagerInterface = ChatActionsManager(
    anivCheckChatAction = AnivCheckChatAction(
        anivContentScanner = anivContentScanner,
        anivUserIdProvider = anivUserIdProvider,
        timber = timber,
        twitchApiService = twitchApiService,
        twitchHandleProvider = authRepository,
        twitchTokensRepository = twitchTokensRepository,
        twitchUtils = twitchUtils,
        userIdsRepository = userIdsRepository
    ),
    catJamChatAction = catJamChatAction,
    chatLoggerChatAction = chatLoggerChatAction,
    cheerActionsWizardChatAction = cheerActionsWizardChatAction,
    deerForceChatAction = DeerForceChatAction(
        generalSettingsRepository = generalSettingsRepository,
        timber = timber,
        twitchUtils = twitchUtils
    ),
    generalSettingsRepository = generalSettingsRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    persistAllUsersChatAction = persistAllUsersChatAction,
    recurringActionsWizardChatAction = recurringActionsWizardChatAction,
    saveMostRecentAnivMessageChatAction = saveMostRecentAnivMessageChatAction,
    schubertWalkChatAction = SchubertWalkChatAction(
        generalSettingsRepository = generalSettingsRepository,
        timber = timber,
        twitchUtils = twitchUtils
    ),
    supStreamerChatAction = None,
    timber = timber,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)


##########################################
## Twitch events initialization section ##
##########################################

twitchCheerHandler: AbsTwitchCheerHandler | None = TwitchCheerHandler(
    cheerActionHelper = cheerActionHelper,
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    triviaGameBuilder = triviaGameBuilder,
    triviaGameMachine = triviaGameMachine
)

twitchRaidHandler: AbsTwitchRaidHandler | None = TwitchRaidHandler(
    chatLogger = chatLogger,
    streamAlertsManager = streamAlertsManager,
    timber = timber
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    twitchCheerHandler = twitchCheerHandler,
    twitchRaidHandler = twitchRaidHandler,
    additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
    administratorProvider = administratorProvider,
    anivCopyMessageTimeoutScorePresenter = anivCopyMessageTimeoutScorePresenter,
    anivCopyMessageTimeoutScoreRepository = anivCopyMessageTimeoutScoreRepository,
    anivSettingsRepository = anivSettingsRepository,
    authRepository = authRepository,
    backgroundTaskHelper = backgroundTaskHelper,
    bannedTriviaGameControllersRepository = bannedTriviaGameControllersRepository,
    bannedWordsRepository = bannedWordsRepository,
    chatActionsManager = chatActionsManager,
    chatLogger = chatLogger,
    cheerActionHelper = cheerActionHelper,
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionSettingsRepository = cheerActionSettingsRepository,
    cheerActionsRepository = cheerActionsRepository,
    cheerActionsWizard = cheerActionsWizard,
    cutenessPresenter = cutenessPresenter,
    cutenessRepository = cutenessRepository,
    cutenessUtils = cutenessUtils,
    funtoonRepository = funtoonRepository,
    funtoonTokensRepository = funtoonTokensRepository,
    generalSettingsRepository = generalSettingsRepository,
    immediateSoundPlayerManager = immediateSoundPlayerManager,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    jishoHelper = jishoHelper,
    languagesRepository = languagesRepository,
    locationsRepository = locationsRepository,
    modifyUserDataHelper = modifyUserDataHelper,
    mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    openTriviaDatabaseTriviaQuestionRepository = openTriviaDatabaseTriviaQuestionRepository,
    pokepediaRepository = pokepediaRepository,
    recurringActionsHelper = recurringActionsHelper,
    recurringActionsMachine = recurringActionsMachine,
    recurringActionsRepository = recurringActionsRepository,
    recurringActionsWizard = recurringActionsWizard,
    sentMessageLogger = sentMessageLogger,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    starWarsQuotesRepository = starWarsQuotesRepository,
    streamAlertsManager = streamAlertsManager,
    supStreamerRepository = supStreamerRepository,
    timber = timber,
    timeoutCheerActionHelper = timeoutCheerActionHelper,
    timeoutCheerActionHistoryRepository = timeoutCheerActionHistoryRepository,
    toxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository,
    translationHelper = translationHelper,
    triviaBanHelper = triviaBanHelper,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameBuilder = triviaGameBuilder,
    triviaGameControllersRepository = triviaGameControllersRepository,
    triviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository,
    triviaGameMachine = triviaGameMachine,
    triviaHistoryRepository = triviaHistoryRepository,
    triviaIdGenerator = triviaIdGenerator,
    triviaRepository = triviaRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
    triviaUtils = triviaUtils,
    ttsJsonMapper = ttsJsonMapper,
    ttsSettingsRepository = ttsSettingsRepository,
    twitchApiService = twitchApiService,
    twitchChannelJoinHelper = twitchChannelJoinHelper,
    twitchConfiguration = twitchConfiguration,
    twitchEmotesHelper = twitchEmotesHelper,
    twitchFollowingStatusRepository = twitchFollowingStatusRepository,
    twitchPredictionWebsocketUtils = TwitchPredictionWebsocketUtils(),
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    twitchTokensRepository = twitchTokensRepository,
    twitchTokensUtils = twitchTokensUtils,
    twitchUtils = twitchUtils,
    twitchWebsocketClient = twitchWebsocketClient,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    weatherReportPresenter = weatherReportPresenter,
    weatherRepository = weatherRepository,
    websocketConnectionServer = None,
    wordOfTheDayPresenter = wordOfTheDayPresenter,
    wordOfTheDayRepository = wordOfTheDayRepository
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
