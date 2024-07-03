import asyncio
import locale
import logging
from asyncio import AbstractEventLoop

from misc.administratorProvider import AdministratorProvider
from misc.administratorProviderInterface import AdministratorProviderInterface
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
from misc.authRepository import AuthRepository
from chatActions.chatActionsManager import ChatActionsManager
from chatActions.chatActionsManagerInterface import ChatActionsManagerInterface
from chatActions.cheerActionsWizardChatAction import \
    CheerActionsWizardChatAction
from chatActions.persistAllUsersChatAction import PersistAllUsersChatAction
from chatActions.saveMostRecentAnivMessageChatAction import \
    SaveMostRecentAnivMessageChatAction
from chatActions.supStreamerChatAction import SupStreamerChatAction
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
from cynanBot import CynanBot
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
from misc.generalSettingsRepository import GeneralSettingsRepository
from google.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from google.googleApiService import GoogleApiService
from google.googleApiServiceInterface import GoogleApiServiceInterface
from google.googleJsonMapper import GoogleJsonMapper
from google.googleJsonMapperInterface import GoogleJsonMapperInterface
from google.googleJwtBuilder import GoogleJwtBuilder
from google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from language.languagesRepository import LanguagesRepository
from language.languagesRepositoryInterface import LanguagesRepositoryInterface
from location.locationsRepository import LocationsRepository
from location.locationsRepositoryInterface import LocationsRepositoryInterface
from location.timeZoneRepository import TimeZoneRepository
from location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from misc.backgroundTaskHelper import BackgroundTaskHelper
from mostRecentChat.mostRecentChatsRepository import MostRecentChatsRepository
from mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from network.aioHttpClientProvider import AioHttpClientProvider
from network.networkClientProvider import NetworkClientProvider
from network.networkClientType import NetworkClientType
from network.requestsClientProvider import RequestsClientProvider
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
from websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface

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

backgroundTaskHelper: BackgroundTaskHelper = BackgroundTaskHelper(
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

websocketConnectionServer: WebsocketConnectionServerInterface = WebsocketConnectionServer(
    backgroundTaskHelper = backgroundTaskHelper,
    settingsJsonReader = JsonFileReader('websocketConnectionServer.json'),
    timber = timber,
    timeZoneRepository = timeZoneRepository,
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

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

googleJwtBuilder: GoogleJwtBuilderInterface = GoogleJwtBuilder(
    googleCloudCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    timeZoneRepository = timeZoneRepository,
)

googleApiService: GoogleApiServiceInterface = GoogleApiService(
    googleApiAccessTokenStorage = googleApiAccessTokenStorage,
    googleCloudProjectCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    googleJwtBuilder = googleJwtBuilder,
    networkClientProvider = networkClientProvider,
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

supStreamerChatAction: SupStreamerChatAction | None = None
if streamAlertsManager is not None:
    supStreamerChatAction = SupStreamerChatAction(
        streamAlertsManager = streamAlertsManager,
        supStreamerRepository = supStreamerRepository,
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

chatActionsManager: ChatActionsManagerInterface = ChatActionsManager(
    anivCheckChatAction = None,
    catJamChatAction = None,
    chatLoggerChatAction = None,
    cheerActionsWizardChatAction = cheerActionsWizardChatAction,
    deerForceChatAction = None,
    generalSettingsRepository = generalSettingsRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    persistAllUsersChatAction = persistAllUsersChatAction,
    recurringActionsWizardChatAction = None,
    saveMostRecentAnivMessageChatAction = saveMostRecentAnivMessageChatAction,
    schubertWalkChatAction = None,
    supStreamerChatAction = supStreamerChatAction,
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
    triviaGameBuilder = None,
    triviaGameMachine = None
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
    additionalTriviaAnswersRepository = None,
    administratorProvider = administratorProvider,
    anivCopyMessageTimeoutScorePresenter = anivCopyMessageTimeoutScorePresenter,
    anivCopyMessageTimeoutScoreRepository = anivCopyMessageTimeoutScoreRepository,
    anivSettingsRepository = anivSettingsRepository,
    authRepository = authRepository,
    backgroundTaskHelper = backgroundTaskHelper,
    bannedTriviaGameControllersRepository = None,
    bannedWordsRepository = bannedWordsRepository,
    chatActionsManager = chatActionsManager,
    chatLogger = chatLogger,
    cheerActionHelper = cheerActionHelper,
    cheerActionIdGenerator = cheerActionIdGenerator,
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionsRepository = cheerActionsRepository,
    cheerActionsWizard = cheerActionsWizard,
    cutenessRepository = None,
    cutenessUtils = None,
    funtoonRepository = funtoonRepository,
    funtoonTokensRepository = funtoonTokensRepository,
    generalSettingsRepository = generalSettingsRepository,
    immediateSoundPlayerManager = immediateSoundPlayerManager,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    jishoHelper = None,
    languagesRepository = languagesRepository,
    locationsRepository = locationsRepository,
    modifyUserDataHelper = modifyUserDataHelper,
    mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    openTriviaDatabaseTriviaQuestionRepository = None,
    pokepediaRepository = None,
    recurringActionsHelper = None,
    recurringActionsMachine = None,
    recurringActionsRepository = None,
    recurringActionsWizard = None,
    sentMessageLogger = sentMessageLogger,
    shinyTriviaOccurencesRepository = None,
    soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    starWarsQuotesRepository = None,
    streamAlertsManager = streamAlertsManager,
    supStreamerRepository = supStreamerRepository,
    timber = timber,
    timeoutCheerActionHelper = timeoutCheerActionHelper,
    timeoutCheerActionHistoryRepository = timeoutCheerActionHistoryRepository,
    toxicTriviaOccurencesRepository = None,
    translationHelper = None,
    triviaBanHelper = None,
    triviaEmoteGenerator = None,
    triviaGameBuilder = None,
    triviaGameControllersRepository = None,
    triviaGameGlobalControllersRepository = None,
    triviaGameMachine = None,
    triviaHistoryRepository = None,
    triviaIdGenerator = None,
    triviaRepository = None,
    triviaScoreRepository = None,
    triviaSettingsRepository = None,
    triviaUtils = None,
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
    weatherReportPresenter = None,
    weatherRepository = None,
    websocketConnectionServer = websocketConnectionServer,
    wordOfTheDayPresenter = None,
    wordOfTheDayRepository = None
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
