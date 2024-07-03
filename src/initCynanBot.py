import asyncio
import locale
from asyncio import AbstractEventLoop

from aniv.anivContentScanner import AnivContentScanner
from aniv.anivContentScannerInterface import AnivContentScannerInterface
from aniv.anivCopyMessageTimeoutScorePresenter import \
    AnivCopyMessageTimeoutScorePresenter
from aniv.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from aniv.anivCopyMessageTimeoutScoreRepository import \
    AnivCopyMessageTimeoutScoreRepository
from aniv.anivCopyMessageTimeoutScoreRepositoryInterface import \
    AnivCopyMessageTimeoutScoreRepositoryInterface
from aniv.anivSettingsRepository import AnivSettingsRepository
from aniv.anivSettingsRepositoryInterface import \
    AnivSettingsRepositoryInterface
from aniv.anivUserIdProvider import AnivUserIdProvider
from aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from aniv.mostRecentAnivMessageRepository import \
    MostRecentAnivMessageRepository
from aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from aniv.mostRecentAnivMessageTimeoutHelper import \
    MostRecentAnivMessageTimeoutHelper
from aniv.mostRecentAnivMessageTimeoutHelperInterface import \
    MostRecentAnivMessageTimeoutHelperInterface
from chatActions.anivCheckChatAction import AnivCheckChatAction
from chatActions.catJamChatAction import CatJamChatAction
from chatActions.chatActionsManager import ChatActionsManager
from chatActions.chatActionsManagerInterface import ChatActionsManagerInterface
from chatActions.chatLoggerChatAction import ChatLoggerChatAction
from chatActions.cheerActionsWizardChatAction import \
    CheerActionsWizardChatAction
from chatActions.deerForceChatAction import DeerForceChatAction
from chatActions.persistAllUsersChatAction import PersistAllUsersChatAction
from chatActions.recurringActionsWizardChatAction import \
    RecurringActionsWizardChatAction
from chatActions.saveMostRecentAnivMessageChatAction import \
    SaveMostRecentAnivMessageChatAction
from chatActions.schubertWalkChatAction import SchubertWalkChatAction
from chatLogger.chatLogger import ChatLogger
from chatLogger.chatLoggerInterface import ChatLoggerInterface
from cheerActions.cheerActionHelper import CheerActionHelper
from cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from cheerActions.cheerActionIdGenerator import CheerActionIdGenerator
from cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from cheerActions.cheerActionJsonMapperInterface import \
    CheerActionJsonMapperInterface
from cheerActions.cheerActionsRepository import CheerActionsRepository
from cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from cheerActions.cheerActionsWizard import CheerActionsWizard
from cheerActions.cheerActionsWizardInterface import \
    CheerActionsWizardInterface
from cheerActions.soundAlert.soundAlertCheerActionHelper import \
    SoundAlertCheerActionHelper
from cheerActions.soundAlert.soundAlertCheerActionHelperInterface import \
    SoundAlertCheerActionHelperInterface
from cheerActions.timeout.timeoutCheerActionHelper import \
    TimeoutCheerActionHelper
from cheerActions.timeout.timeoutCheerActionHelperInterface import \
    TimeoutCheerActionHelperInterface
from cheerActions.timeout.timeoutCheerActionHistoryRepository import \
    TimeoutCheerActionHistoryRepository
from cheerActions.timeout.timeoutCheerActionHistoryRepositoryInterface import \
    TimeoutCheerActionHistoryRepositoryInterface
from cheerActions.timeout.timeoutCheerActionJsonMapper import \
    TimeoutCheerActionJsonMapper
from cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from contentScanner.bannedWordsRepository import BannedWordsRepository
from contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from contentScanner.contentScanner import ContentScanner
from contentScanner.contentScannerInterface import ContentScannerInterface
from cuteness.cutenessRepository import CutenessRepository
from cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from cuteness.cutenessUtils import CutenessUtils
from cynanBot import CynanBot
from deepL.deepLApiService import DeepLApiService
from deepL.deepLApiServiceInterface import DeepLApiServiceInterface
from deepL.deepLJsonMapper import DeepLJsonMapper
from deepL.deepLJsonMapperInterface import DeepLJsonMapperInterface
from emojiHelper.emojiHelper import EmojiHelper
from emojiHelper.emojiHelperInterface import EmojiHelperInterface
from emojiHelper.emojiRepository import EmojiRepository
from emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from funtoon.funtoonJsonMapper import FuntoonJsonMapper
from funtoon.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from funtoon.funtoonRepository import FuntoonRepository
from funtoon.funtoonRepositoryInterface import FuntoonRepositoryInterface
from funtoon.funtoonTokensRepository import FuntoonTokensRepository
from funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from google.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from google.googleApiService import GoogleApiService
from google.googleApiServiceInterface import GoogleApiServiceInterface
from google.googleJsonMapper import GoogleJsonMapper
from google.googleJsonMapperInterface import GoogleJsonMapperInterface
from google.googleJwtBuilder import GoogleJwtBuilder
from google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from jisho.jishoApiService import JishoApiService
from jisho.jishoApiServiceInterface import JishoApiServiceInterface
from jisho.jishoJsonMapper import JishoJsonMapper
from jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from jisho.jishoPresenter import JishoPresenter
from jisho.jishoPresenterInterface import JishoPresenterInterface
from language.jishoHelper import JishoHelper
from language.jishoHelperInterface import JishoHelperInterface
from language.languagesRepository import LanguagesRepository
from language.languagesRepositoryInterface import LanguagesRepositoryInterface
from language.translation.deepLTranslationApi import DeepLTranslationApi
from language.translation.googleTranslationApi import GoogleTranslationApi
from language.translation.translationApi import TranslationApi
from language.translationHelper import TranslationHelper
from language.translationHelperInterface import TranslationHelperInterface
from language.wordOfTheDayPresenter import WordOfTheDayPresenter
from language.wordOfTheDayPresenterInterface import \
    WordOfTheDayPresenterInterface
from language.wordOfTheDayRepository import WordOfTheDayRepository
from language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from location.locationsRepository import LocationsRepository
from location.locationsRepositoryInterface import LocationsRepositoryInterface
from location.timeZoneRepository import TimeZoneRepository
from location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from misc.administratorProvider import AdministratorProvider
from misc.administratorProviderInterface import AdministratorProviderInterface
from misc.authRepository import AuthRepository
from misc.backgroundTaskHelper import BackgroundTaskHelper
from misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from misc.generalSettingsRepository import GeneralSettingsRepository
from mostRecentChat.mostRecentChatsRepository import MostRecentChatsRepository
from mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from network.aioHttpClientProvider import AioHttpClientProvider
from network.networkClientProvider import NetworkClientProvider
from network.networkClientType import NetworkClientType
from network.requestsClientProvider import RequestsClientProvider
from openWeather.openWeatherApiService import OpenWeatherApiService
from openWeather.openWeatherApiServiceInterface import \
    OpenWeatherApiServiceInterface
from openWeather.openWeatherJsonMapper import OpenWeatherJsonMapper
from openWeather.openWeatherJsonMapperInterface import \
    OpenWeatherJsonMapperInterface
from pkmn.pokepediaJsonMapper import PokepediaJsonMapper
from pkmn.pokepediaJsonMapperInterface import PokepediaJsonMapperInterface
from pkmn.pokepediaRepository import PokepediaRepository
from pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from recurringActions.mostRecentRecurringActionRepository import \
    MostRecentRecurringActionRepository
from recurringActions.mostRecentRecurringActionRepositoryInterface import \
    MostRecentRecurringActionRepositoryInterface
from recurringActions.recurringActionsHelper import RecurringActionsHelper
from recurringActions.recurringActionsHelperInterface import \
    RecurringActionsHelperInterface
from recurringActions.recurringActionsJsonParser import \
    RecurringActionsJsonParser
from recurringActions.recurringActionsMachine import RecurringActionsMachine
from recurringActions.recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from recurringActions.recurringActionsRepository import \
    RecurringActionsRepository
from recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from recurringActions.recurringActionsWizard import RecurringActionsWizard
from recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from sentMessageLogger.sentMessageLogger import SentMessageLogger
from sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from soundPlayerManager.immediateSoundPlayerManager import \
    ImmediateSoundPlayerManager
from soundPlayerManager.immediateSoundPlayerManagerInterface import \
    ImmediateSoundPlayerManagerInterface
from soundPlayerManager.soundAlertJsonMapper import SoundAlertJsonMapper
from soundPlayerManager.soundAlertJsonMapperInterface import \
    SoundAlertJsonMapperInterface
from soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from soundPlayerManager.soundPlayerManagerProviderInterface import \
    SoundPlayerManagerProviderInterface
from soundPlayerManager.soundPlayerRandomizerHelper import \
    SoundPlayerRandomizerHelper
from soundPlayerManager.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from soundPlayerManager.soundPlayerSettingsRepository import \
    SoundPlayerSettingsRepository
from soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from soundPlayerManager.vlc.vlcSoundPlayerManagerProvider import \
    VlcSoundPlayerManagerProvider
from starWars.starWarsQuotesRepository import StarWarsQuotesRepository
from starWars.starWarsQuotesRepositoryInterface import \
    StarWarsQuotesRepositoryInterface
from storage.backingDatabase import BackingDatabase
from storage.backingPsqlDatabase import BackingPsqlDatabase
from storage.backingSqliteDatabase import BackingSqliteDatabase
from storage.databaseType import DatabaseType
from storage.jsonFileReader import JsonFileReader
from storage.linesFileReader import LinesFileReader
from storage.psqlCredentialsProvider import PsqlCredentialsProvider
from streamAlertsManager.streamAlertsManager import StreamAlertsManager
from streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from streamAlertsManager.streamAlertsSettingsRepository import \
    StreamAlertsSettingsRepository
from streamAlertsManager.streamAlertsSettingsRepositoryInterface import \
    StreamAlertsSettingsRepositoryInterface
from supStreamer.supStreamerRepository import SupStreamerRepository
from supStreamer.supStreamerRepositoryInterface import \
    SupStreamerRepositoryInterface
from systemCommandHelper.systemCommandHelper import SystemCommandHelper
from systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
from timber.timber import Timber
from timber.timberInterface import TimberInterface
from transparent.transparentApiService import TransparentApiService
from transparent.transparentApiServiceInterface import \
    TransparentApiServiceInterface
from transparent.transparentXmlMapper import TransparentXmlMapper
from transparent.transparentXmlMapperInterface import \
    TransparentXmlMapperInterface
from trivia.additionalAnswers.additionalTriviaAnswersRepository import \
    AdditionalTriviaAnswersRepository
from trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from trivia.banned.bannedTriviaGameControllersRepository import \
    BannedTriviaGameControllersRepository
from trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from trivia.banned.bannedTriviaIdsRepository import BannedTriviaIdsRepository
from trivia.banned.bannedTriviaIdsRepositoryInterface import \
    BannedTriviaIdsRepositoryInterface
from trivia.banned.triviaBanHelper import TriviaBanHelper
from trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from trivia.builder.triviaGameBuilder import TriviaGameBuilder
from trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from trivia.content.triviaContentScanner import TriviaContentScanner
from trivia.content.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from trivia.emotes.triviaEmoteGenerator import TriviaEmoteGenerator
from trivia.emotes.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from trivia.emotes.triviaEmoteRepository import TriviaEmoteRepository
from trivia.emotes.triviaEmoteRepositoryInterface import \
    TriviaEmoteRepositoryInterface
from trivia.gameController.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from trivia.gameController.triviaGameGlobalControllersRepository import \
    TriviaGameGlobalControllersRepository
from trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from trivia.games.triviaGameStore import TriviaGameStore
from trivia.score.triviaScoreRepository import TriviaScoreRepository
from trivia.score.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from trivia.scraper.triviaScraper import TriviaScraper
from trivia.scraper.triviaScraperInterface import TriviaScraperInterface
from trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from trivia.specialStatus.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import \
    ShinyTriviaOccurencesRepositoryInterface
from trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from trivia.specialStatus.toxicTriviaOccurencesRepository import \
    ToxicTriviaOccurencesRepository
from trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import \
    ToxicTriviaOccurencesRepositoryInterface
from trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from trivia.triviaAnswerChecker import TriviaAnswerChecker
from trivia.triviaGameMachine import TriviaGameMachine
from trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from trivia.triviaHistoryRepository import TriviaHistoryRepository
from trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from trivia.triviaIdGenerator import TriviaIdGenerator
from trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from trivia.triviaQuestionPresenter import TriviaQuestionPresenter
from trivia.triviaQuestionPresenterInterface import \
    TriviaQuestionPresenterInterface
from trivia.triviaRepositories.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from trivia.triviaRepositories.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from trivia.triviaRepositories.glacialTriviaQuestionRepository import \
    GlacialTriviaQuestionRepository
from trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from trivia.triviaRepositories.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from trivia.triviaRepositories.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from trivia.triviaRepositories.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from trivia.triviaRepositories.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from trivia.triviaRepositories.triviaRepository import TriviaRepository
from trivia.triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from trivia.triviaRepositories.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from trivia.triviaRepositories.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from trivia.triviaSettingsRepository import TriviaSettingsRepository
from trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from trivia.triviaSourceInstabilityHelper import TriviaSourceInstabilityHelper
from trivia.triviaUtils import TriviaUtils
from trivia.triviaUtilsInterface import TriviaUtilsInterface
from trivia.triviaVerifier import TriviaVerifier
from trivia.triviaVerifierInterface import TriviaVerifierInterface
from tts.decTalk.decTalkFileManager import DecTalkFileManager
from tts.decTalk.decTalkFileManagerInterface import DecTalkFileManagerInterface
from tts.decTalk.decTalkManager import DecTalkManager
from tts.decTalk.decTalkVoiceChooser import DecTalkVoiceChooser
from tts.decTalk.decTalkVoiceChooserInterface import \
    DecTalkVoiceChooserInterface
from tts.decTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from tts.decTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from tts.google.googleFileExtensionHelper import GoogleFileExtensionHelper
from tts.google.googleFileExtensionHelperInterface import \
    GoogleFileExtensionHelperInterface
from tts.google.googleTtsFileManager import GoogleTtsFileManager
from tts.google.googleTtsFileManagerInterface import \
    GoogleTtsFileManagerInterface
from tts.google.googleTtsManager import GoogleTtsManager
from tts.google.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from tts.google.googleTtsVoiceChooserInterface import \
    GoogleTtsVoiceChooserInterface
from tts.tempFileHelper.ttsTempFileHelper import TtsTempFileHelper
from tts.tempFileHelper.ttsTempFileHelperInterface import \
    TtsTempFileHelperInterface
from tts.ttsCommandBuilder import TtsCommandBuilder
from tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from tts.ttsManager import TtsManager
from tts.ttsManagerInterface import TtsManagerInterface
from tts.ttsSettingsRepository import TtsSettingsRepository
from tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from twitch.api.twitchApiService import TwitchApiService
from twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from twitch.api.twitchJsonMapper import TwitchJsonMapper
from twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from twitch.configuration.twitchChannelJoinHelper import \
    TwitchChannelJoinHelper
from twitch.configuration.twitchCheerHandler import TwitchCheerHandler
from twitch.configuration.twitchConfiguration import TwitchConfiguration
from twitch.configuration.twitchIo.twitchIoConfiguration import \
    TwitchIoConfiguration
from twitch.configuration.twitchRaidHandler import TwitchRaidHandler
from twitch.followingStatus.twitchFollowingStatusRepository import \
    TwitchFollowingStatusRepository
from twitch.followingStatus.twitchFollowingStatusRepositoryInterface import \
    TwitchFollowingStatusRepositoryInterface
from twitch.isLiveOnTwitchRepository import IsLiveOnTwitchRepository
from twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from twitch.timeout.timeoutImmuneUserIdsRepository import \
    TimeoutImmuneUserIdsRepository
from twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import \
    TimeoutImmuneUserIdsRepositoryInterface
from twitch.timeout.twitchTimeoutHelper import TwitchTimeoutHelper
from twitch.timeout.twitchTimeoutHelperInterface import \
    TwitchTimeoutHelperInterface
from twitch.timeout.twitchTimeoutRemodHelper import TwitchTimeoutRemodHelper
from twitch.timeout.twitchTimeoutRemodHelperInterface import \
    TwitchTimeoutRemodHelperInterface
from twitch.timeout.twitchTimeoutRemodRepository import \
    TwitchTimeoutRemodRepository
from twitch.timeout.twitchTimeoutRemodRepositoryInterface import \
    TwitchTimeoutRemodRepositoryInterface
from twitch.twitchAnonymousUserIdProvider import TwitchAnonymousUserIdProvider
from twitch.twitchAnonymousUserIdProviderInterface import \
    TwitchAnonymousUserIdProviderInterface
from twitch.twitchChannelJoinHelperInterface import \
    TwitchChannelJoinHelperInterface
from twitch.twitchPredictionWebsocketUtils import \
    TwitchPredictionWebsocketUtils
from twitch.twitchTokensRepository import TwitchTokensRepository
from twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from twitch.twitchTokensUtils import TwitchTokensUtils
from twitch.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from twitch.twitchUtils import TwitchUtils
from twitch.twitchUtilsInterface import TwitchUtilsInterface
from twitch.websocket.twitchWebsocketAllowedUsersRepository import \
    TwitchWebsocketAllowedUsersRepository
from twitch.websocket.twitchWebsocketClient import TwitchWebsocketClient
from twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from twitch.websocket.twitchWebsocketJsonMapper import \
    TwitchWebsocketJsonMapper
from twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from users.modifyUserDataHelper import ModifyUserDataHelper
from users.userIdsRepository import UserIdsRepository
from users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from users.usersRepository import UsersRepository
from users.usersRepositoryInterface import UsersRepositoryInterface
from weather.weatherReportPresenter import WeatherReportPresenter
from weather.weatherReportPresenterInterface import \
    WeatherReportPresenterInterface
from weather.weatherRepository import WeatherRepository
from weather.weatherRepositoryInterface import WeatherRepositoryInterface

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
