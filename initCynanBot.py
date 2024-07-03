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
from src.cheerActions.cheerActionHelper import CheerActionHelper
from src.cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from src.cheerActions.cheerActionIdGenerator import CheerActionIdGenerator
from src.cheerActions.cheerActionIdGeneratorInterface import CheerActionIdGeneratorInterface
from src.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from src.cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
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
from src.cuteness.cutenessRepository import CutenessRepository
from src.cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from src.cuteness.cutenessUtils import CutenessUtils
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
from src.language.translation.translationApi import TranslationApi
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
from src.misc.generalSettingsRepository import GeneralSettingsRepository
from src.mostRecentChat.mostRecentChatsRepository import MostRecentChatsRepository
from src.mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from src.network.aioHttpClientProvider import AioHttpClientProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.network.networkClientType import NetworkClientType
from src.network.requestsClientProvider import RequestsClientProvider
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
from src.streamAlertsManager.streamAlertsManager import StreamAlertsManager
from src.streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from src.streamAlertsManager.streamAlertsSettingsRepository import StreamAlertsSettingsRepository
from src.streamAlertsManager.streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface
from src.systemCommandHelper.systemCommandHelper import SystemCommandHelper
from src.systemCommandHelper.systemCommandHelperInterface import SystemCommandHelperInterface
from src.timbertimber import Timber
from src.timbertimberInterface import TimberInterface
from src.transparent.transparentApiService import TransparentApiService
from src.transparent.transparentApiServiceInterface import TransparentApiServiceInterface
from src.transparent.transparentXmlMapper import TransparentXmlMapper
from src.transparent.transparentXmlMapperInterface import TransparentXmlMapperInterface
from src.triviaadditionalAnswers.additionalTriviaAnswersRepository import AdditionalTriviaAnswersRepository
from src.triviaadditionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from src.triviabanned.bannedTriviaGameControllersRepository import BannedTriviaGameControllersRepository
from src.triviabanned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from src.triviabanned.bannedTriviaIdsRepository import BannedTriviaIdsRepository
from src.triviabanned.bannedTriviaIdsRepositoryInterface import BannedTriviaIdsRepositoryInterface
from src.triviabanned.triviaBanHelper import TriviaBanHelper
from src.triviabanned.triviaBanHelperInterface import TriviaBanHelperInterface
from src.triviabuilder.triviaGameBuilder import TriviaGameBuilder
from src.triviabuilder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from src.triviacompilers.triviaAnswerCompiler import TriviaAnswerCompiler
from src.triviacompilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from src.triviacompilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.triviacompilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from src.triviacontent.triviaContentScanner import TriviaContentScanner
from src.triviacontent.triviaContentScannerInterface import TriviaContentScannerInterface
from src.triviaemotes.triviaEmoteGenerator import TriviaEmoteGenerator
from src.triviaemotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from src.triviaemotes.triviaEmoteRepository import TriviaEmoteRepository
from src.triviaemotes.triviaEmoteRepositoryInterface import TriviaEmoteRepositoryInterface
from src.triviagameController.triviaGameControllersRepository import TriviaGameControllersRepository
from src.triviagameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from src.triviagameController.triviaGameGlobalControllersRepository import TriviaGameGlobalControllersRepository
from src.triviagameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from src.triviagames.queuedTriviaGameStore import QueuedTriviaGameStore
from src.triviagames.triviaGameStore import TriviaGameStore
from src.triviascore.triviaScoreRepository import TriviaScoreRepository
from src.triviascore.triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from src.triviascraper.triviaScraper import TriviaScraper
from src.triviascraper.triviaScraperInterface import TriviaScraperInterface
from src.triviaspecialStatus.shinyTriviaHelper import ShinyTriviaHelper
from src.triviaspecialStatus.shinyTriviaOccurencesRepository import ShinyTriviaOccurencesRepository
from src.triviaspecialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from src.triviaspecialStatus.toxicTriviaHelper import ToxicTriviaHelper
from src.triviaspecialStatus.toxicTriviaOccurencesRepository import ToxicTriviaOccurencesRepository
from src.triviaspecialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from src.triviasuperTriviaCooldownHelper import SuperTriviaCooldownHelper
from src.triviatriviaAnswerChecker import TriviaAnswerChecker
from src.triviatriviaGameMachine import TriviaGameMachine
from src.triviatriviaGameMachineInterface import TriviaGameMachineInterface
from src.triviatriviaHistoryRepository import TriviaHistoryRepository
from src.triviatriviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from src.triviatriviaIdGenerator import TriviaIdGenerator
from src.triviatriviaIdGeneratorInterface import TriviaIdGeneratorInterface
from src.triviatriviaQuestionPresenter import TriviaQuestionPresenter
from src.triviatriviaQuestionPresenterInterface import TriviaQuestionPresenterInterface
from src.triviatriviaRepositories.bongoTriviaQuestionRepository import BongoTriviaQuestionRepository
from src.triviatriviaRepositories.funtoonTriviaQuestionRepository import FuntoonTriviaQuestionRepository
from src.triviatriviaRepositories.glacialTriviaQuestionRepository import GlacialTriviaQuestionRepository
from src.triviatriviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from src.triviatriviaRepositories.jServiceTriviaQuestionRepository import JServiceTriviaQuestionRepository
from src.triviatriviaRepositories.lotrTriviaQuestionsRepository import LotrTriviaQuestionRepository
from src.triviatriviaRepositories.millionaireTriviaQuestionRepository import MillionaireTriviaQuestionRepository
from src.triviatriviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from src.triviatriviaRepositories.openTriviaQaTriviaQuestionRepository import OpenTriviaQaTriviaQuestionRepository
from src.triviatriviaRepositories.pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from src.triviatriviaRepositories.quizApiTriviaQuestionRepository import QuizApiTriviaQuestionRepository
from src.triviatriviaRepositories.triviaDatabaseTriviaQuestionRepository import TriviaDatabaseTriviaQuestionRepository
from src.triviatriviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from src.triviatriviaRepositories.triviaRepository import TriviaRepository
from src.triviatriviaRepositories.triviaRepositoryInterface import TriviaRepositoryInterface
from src.triviatriviaRepositories.willFryTriviaQuestionRepository import WillFryTriviaQuestionRepository
from src.triviatriviaRepositories.wwtbamTriviaQuestionRepository import WwtbamTriviaQuestionRepository
from src.triviatriviaSettingsRepository import TriviaSettingsRepository
from src.triviatriviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from src.triviatriviaSourceInstabilityHelper import TriviaSourceInstabilityHelper
from src.triviatriviaUtils import TriviaUtils
from src.triviatriviaUtilsInterface import TriviaUtilsInterface
from src.triviatriviaVerifier import TriviaVerifier
from src.triviatriviaVerifierInterface import TriviaVerifierInterface
from src.ttsdecTalk.decTalkFileManager import DecTalkFileManager
from src.ttsdecTalk.decTalkFileManagerInterface import DecTalkFileManagerInterface
from src.ttsdecTalk.decTalkManager import DecTalkManager
from src.ttsdecTalk.decTalkVoiceChooser import DecTalkVoiceChooser
from src.ttsdecTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from src.ttsdecTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from src.ttsdecTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.ttsgoogle.googleFileExtensionHelper import GoogleFileExtensionHelper
from src.ttsgoogle.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from src.ttsgoogle.googleTtsFileManager import GoogleTtsFileManager
from src.ttsgoogle.googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from src.ttsgoogle.googleTtsManager import GoogleTtsManager
from src.ttsgoogle.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from src.ttsgoogle.googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from src.ttstempFileHelper.ttsTempFileHelper import TtsTempFileHelper
from src.ttstempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from src.ttsttsCommandBuilder import TtsCommandBuilder
from src.ttsttsCommandBuilderInterface import TtsCommandBuilderInterface
from src.ttsttsManager import TtsManager
from src.ttsttsManagerInterface import TtsManagerInterface
from src.ttsttsSettingsRepository import TtsSettingsRepository
from src.ttsttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
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
from src.twitchabsTwitchCheerHandler import AbsTwitchCheerHandler
from src.twitchabsTwitchRaidHandler import AbsTwitchRaidHandler
from src.twitchapi.twitchApiService import TwitchApiService
from src.twitchapi.twitchApiServiceInterface import TwitchApiServiceInterface
from src.twitchapi.twitchJsonMapper import TwitchJsonMapper
from src.twitchapi.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitchconfiguration.twitchChannelJoinHelper import TwitchChannelJoinHelper
from src.twitchconfiguration.twitchCheerHandler import TwitchCheerHandler
from src.twitchconfiguration.twitchConfiguration import TwitchConfiguration
from src.twitchconfiguration.twitchIo.twitchIoConfiguration import TwitchIoConfiguration
from src.twitchconfiguration.twitchRaidHandler import TwitchRaidHandler
from src.twitchfollowingStatus.twitchFollowingStatusRepository import TwitchFollowingStatusRepository
from src.twitchfollowingStatus.twitchFollowingStatusRepositoryInterface import \
    TwitchFollowingStatusRepositoryInterface
from src.twitchisLiveOnTwitchRepository import IsLiveOnTwitchRepository
from src.twitchisLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from src.twitchtimeout.timeoutImmuneUserIdsRepository import TimeoutImmuneUserIdsRepository
from src.twitchtimeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from src.twitchtimeout.twitchTimeoutHelper import TwitchTimeoutHelper
from src.twitchtimeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from src.twitchtimeout.twitchTimeoutRemodHelper import TwitchTimeoutRemodHelper
from src.twitchtimeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from src.twitchtimeout.twitchTimeoutRemodRepository import TwitchTimeoutRemodRepository
from src.twitchtimeout.twitchTimeoutRemodRepositoryInterface import TwitchTimeoutRemodRepositoryInterface
from src.twitchtwitchAnonymousUserIdProvider import TwitchAnonymousUserIdProvider
from src.twitchtwitchAnonymousUserIdProviderInterface import TwitchAnonymousUserIdProviderInterface
from src.users.modifyUserDataHelper import ModifyUserDataHelper
from src.users.userIdsRepository import UserIdsRepository
from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from src.users.usersRepository import UsersRepository
from src.users.usersRepositoryInterface import UsersRepositoryInterface
from src.weather.weatherReportPresenter import WeatherReportPresenter
from src.weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from src.weather.weatherRepository import WeatherRepository
from src.weather.weatherRepositoryInterface import WeatherRepositoryInterface
from supStreamer.supStreamerRepository import SupStreamerRepository
from supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface

# Uncomment this chunk to turn on extra extra debug logging
# logging.basicConfig(
#     filename = 'generalLogging.log',
#     level = logging.DEBUG
# )


locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Core initialization section ##
#################################

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper,
    timeZoneRepository = timeZoneRepository
)

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonFileReader('generalSettingsRepository.json')
)

generalSettingsSnapshot = generalSettingsRepository.getAll()

backingDatabase: BackingDatabase
if generalSettingsSnapshot.requireDatabaseType() is DatabaseType.POSTGRESQL:
    backingDatabase: BackingDatabase = BackingPsqlDatabase(
        eventLoop = eventLoop,
        psqlCredentialsProvider = PsqlCredentialsProvider(
            credentialsJsonReader = JsonFileReader('psqlCredentials.json')
        ),
        timber = timber
    )
elif generalSettingsSnapshot.requireDatabaseType() is DatabaseType.SQLITE:
    backingDatabase: BackingDatabase = BackingSqliteDatabase(
        eventLoop = eventLoop
    )
else:
    raise RuntimeError(f'Unknown/misconfigured database type: \"{generalSettingsSnapshot.requireDatabaseType()}\"')

networkClientProvider: NetworkClientProvider
if generalSettingsSnapshot.requireNetworkClientType() is NetworkClientType.AIOHTTP:
    networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
        eventLoop = eventLoop,
        timber = timber
    )
elif generalSettingsSnapshot.requireNetworkClientType() is NetworkClientType.REQUESTS:
    networkClientProvider: NetworkClientProvider = RequestsClientProvider(
        timber = timber
    )
else:
    raise RuntimeError(f'Unknown/misconfigured network client type: \"{generalSettingsSnapshot.requireNetworkClientType()}\"')

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

cutenessRepository: CutenessRepositoryInterface = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)
emojiRepository: EmojiRepositoryInterface = EmojiRepository(
    emojiJsonReader = JsonFileReader('emojiRepository.json'),
    timber = timber
)
emojiHelper: EmojiHelperInterface = EmojiHelper(
    emojiRepository = emojiRepository
)

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

timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface =  TimeoutImmuneUserIdsRepository(
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

deepLTranslationApi: TranslationApi = DeepLTranslationApi(
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

googleTranslationApi: TranslationApi = GoogleTranslationApi(
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
triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(
    timber = timber
)
triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
    timber = timber
)
triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()
triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('triviaSettingsRepository.json')
)
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
        twitchHandleProvider = authRepository,
        twitchTimeoutHelper = twitchTimeoutHelper,
        twitchTokensRepository = twitchTokensRepository,
        twitchUtils = twitchUtils
    )


##############################################
## Recurring Actions initialization section ##
##############################################

recurringActionsRepository: RecurringActionsRepositoryInterface = RecurringActionsRepository(
    backingDatabase = backingDatabase,
    recurringActionsJsonParser = RecurringActionsJsonParser(
        languagesRepository = languagesRepository,
        timber = timber
    ),
    timber = timber
)

mostRecentRecurringActionRepository: MostRecentRecurringActionRepositoryInterface = MostRecentRecurringActionRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

recurringActionsMachine: RecurringActionsMachineInterface = RecurringActionsMachine(
    backgroundTaskHelper = backgroundTaskHelper,
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

cheerActionIdGenerator: CheerActionIdGeneratorInterface = CheerActionIdGenerator()

cheerActionJsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
    timber = timber
)

cheerActionsRepository: CheerActionsRepositoryInterface = CheerActionsRepository(
    backingDatabase = backingDatabase,
    cheerActionIdGenerator = cheerActionIdGenerator,
    cheerActionJsonMapper = cheerActionJsonMapper,
    timber = timber
)

cheerActionsWizard: CheerActionsWizardInterface = CheerActionsWizard(
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
    cheerActionIdGenerator = cheerActionIdGenerator,
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionsRepository = cheerActionsRepository,
    cheerActionsWizard = cheerActionsWizard,
    cutenessRepository = cutenessRepository,
    cutenessUtils = CutenessUtils(),
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
    ttsSettingsRepository = ttsSettingsRepository,
    twitchApiService = twitchApiService,
    twitchChannelJoinHelper = twitchChannelJoinHelper,
    twitchConfiguration = twitchConfiguration,
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
