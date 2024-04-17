import asyncio
import locale
import logging
from asyncio import AbstractEventLoop
from typing import Optional

from CynanBot.administratorProvider import AdministratorProvider
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.aniv.anivUserIdProvider import AnivUserIdProvider
from CynanBot.aniv.anivUserIdProviderInterface import \
    AnivUserIdProviderInterface
from CynanBot.aniv.mostRecentAnivMessageRepository import \
    MostRecentAnivMessageRepository
from CynanBot.aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from CynanBot.aniv.mostRecentAnivMessageTimeoutHelper import \
    MostRecentAnivMessageTimeoutHelper
from CynanBot.aniv.mostRecentAnivMessageTimeoutHelperInterface import \
    MostRecentAnivMessageTimeoutHelperInterface
from CynanBot.authRepository import AuthRepository
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.chatActions.chatActionsManager import ChatActionsManager
from CynanBot.chatActions.chatActionsManagerInterface import \
    ChatActionsManagerInterface
from CynanBot.chatActions.persistAllUsersChatAction import \
    PersistAllUsersChatAction
from CynanBot.chatActions.supStreamerChatAction import SupStreamerChatAction
from CynanBot.chatLogger.chatLogger import ChatLogger
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cheerActions.cheerActionHelper import CheerActionHelper
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.cheerActions.cheerActionIdGenerator import CheerActionIdGenerator
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBot.cheerActions.cheerActionsRepository import CheerActionsRepository
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.cynanBot import CynanBot
from CynanBot.dependencyHolderBuilder import DependencyHolderBuilder
from CynanBot.emojiHelper.emojiHelper import EmojiHelper
from CynanBot.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from CynanBot.emojiHelper.emojiRepository import EmojiRepository
from CynanBot.emojiHelper.emojiRepositoryInterface import \
    EmojiRepositoryInterface
from CynanBot.funtoon.funtoonRepository import FuntoonRepository
from CynanBot.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBot.funtoon.funtoonTokensRepository import FuntoonTokensRepository
from CynanBot.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.google.googleApiAccessTokenStorage import \
    GoogleApiAccessTokenStorage
from CynanBot.google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from CynanBot.google.googleApiService import GoogleApiService
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleJsonMapper import GoogleJsonMapper
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleJwtBuilder import GoogleJwtBuilder
from CynanBot.google.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from CynanBot.language.jishoHelper import JishoHelper
from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.location.locationsRepository import LocationsRepository
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.mostRecentChat.mostRecentChatsRepository import \
    MostRecentChatsRepository
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.requestsClientProvider import RequestsClientProvider
from CynanBot.sentMessageLogger.sentMessageLogger import SentMessageLogger
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.soundPlayerManager.channelPoint.channelPointSoundHelper import \
    ChannelPointSoundHelper
from CynanBot.soundPlayerManager.channelPoint.channelPointSoundHelperInterface import \
    ChannelPointSoundHelperInterface
from CynanBot.soundPlayerManager.soundAlertJsonMapper import \
    SoundAlertJsonMapper
from CynanBot.soundPlayerManager.soundAlertJsonMapperInterface import \
    SoundAlertJsonMapperInterface
from CynanBot.soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from CynanBot.soundPlayerManager.soundPlayerSettingsRepository import \
    SoundPlayerSettingsRepository
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.soundPlayerManager.vlc.vlcSoundPlayerManager import \
    VlcSoundPlayerManager
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.backingPsqlDatabase import BackingPsqlDatabase
from CynanBot.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.jsonFileReader import JsonFileReader
from CynanBot.storage.linesFileReader import LinesFileReader
from CynanBot.storage.psqlCredentialsProvider import PsqlCredentialsProvider
from CynanBot.streamAlertsManager.streamAlertsManager import \
    StreamAlertsManager
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.streamAlertsManager.streamAlertsSettingsRepository import \
    StreamAlertsSettingsRepository
from CynanBot.streamAlertsManager.streamAlertsSettingsRepositoryInterface import \
    StreamAlertsSettingsRepositoryInterface
from CynanBot.systemCommandHelper.systemCommandHelper import \
    SystemCommandHelper
from CynanBot.systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
from CynanBot.timber.timber import Timber
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.decTalk.decTalkFileManager import DecTalkFileManager
from CynanBot.tts.decTalk.decTalkManager import DecTalkManager
from CynanBot.tts.google.googleFileExtensionHelper import \
    GoogleFileExtensionHelper
from CynanBot.tts.google.googleFileExtensionHelperInterface import \
    GoogleFileExtensionHelperInterface
from CynanBot.tts.google.googleTtsFileManager import GoogleTtsFileManager
from CynanBot.tts.google.googleTtsFileManagerInterface import \
    GoogleTtsFileManagerInterface
from CynanBot.tts.google.googleTtsManager import GoogleTtsManager
from CynanBot.tts.tempFileHelper.ttsTempFileHelper import TtsTempFileHelper
from CynanBot.tts.tempFileHelper.ttsTempFileHelperInterface import \
    TtsTempFileHelperInterface
from CynanBot.tts.ttsCommandBuilder import TtsCommandBuilder
from CynanBot.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from CynanBot.tts.ttsManager import TtsManager
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.tts.ttsSettingsRepository import TtsSettingsRepository
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface
from CynanBot.twitch.api.twitchApiService import TwitchApiService
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.configuration.channelJoinHelper import ChannelJoinHelper
from CynanBot.twitch.configuration.twitchConfiguration import \
    TwitchConfiguration
from CynanBot.twitch.configuration.twitchIo.twitchIoConfiguration import \
    TwitchIoConfiguration
from CynanBot.twitch.isLiveOnTwitchRepository import IsLiveOnTwitchRepository
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchAnonymousUserIdProvider import \
    TwitchAnonymousUserIdProvider
from CynanBot.twitch.twitchAnonymousUserIdProviderInterface import \
    TwitchAnonymousUserIdProviderInterface
from CynanBot.twitch.twitchFollowerRepository import TwitchFollowerRepository
from CynanBot.twitch.twitchFollowerRepositoryInterface import \
    TwitchFollowerRepositoryInterface
from CynanBot.twitch.twitchPredictionWebsocketUtils import \
    TwitchPredictionWebsocketUtils
from CynanBot.twitch.twitchTimeoutHelper import TwitchTimeoutHelper
from CynanBot.twitch.twitchTimeoutHelperInterface import \
    TwitchTimeoutHelperInterface
from CynanBot.twitch.twitchTimeoutRemodHelper import TwitchTimeoutRemodHelper
from CynanBot.twitch.twitchTimeoutRemodHelperInterface import \
    TwitchTimeoutRemodHelperInterface
from CynanBot.twitch.twitchTimeoutRemodRepository import \
    TwitchTimeoutRemodRepository
from CynanBot.twitch.twitchTimeoutRemodRepositoryInterface import \
    TwitchTimeoutRemodRepositoryInterface
from CynanBot.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchTokensUtils import TwitchTokensUtils
from CynanBot.twitch.twitchTokensUtilsInterface import \
    TwitchTokensUtilsInterface
from CynanBot.twitch.twitchUtils import TwitchUtils
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.twitch.websocket.twitchWebsocketAllowedUsersRepository import \
    TwitchWebsocketAllowedUsersRepository
from CynanBot.twitch.websocket.twitchWebsocketClient import \
    TwitchWebsocketClient
from CynanBot.twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from CynanBot.twitch.websocket.twitchWebsocketJsonMapper import \
    TwitchWebsocketJsonMapper
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from CynanBot.users.modifyUserDataHelper import ModifyUserDataHelper
from CynanBot.users.userIdsRepository import UserIdsRepository
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepository import UsersRepository
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface
from CynanBot.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface

# Uncomment this chunk to turn on extra extra debug logging
# logging.basicConfig(
#     filename = 'generalLogging.log',
#     level = logging.DEBUG
# )


locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Misc initialization section ##
#################################

eventLoop: AbstractEventLoop = asyncio.get_event_loop()
backgroundTaskHelper = BackgroundTaskHelper(eventLoop = eventLoop)
timber: TimberInterface = Timber(backgroundTaskHelper = backgroundTaskHelper)

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
bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader('bannedWords.txt'),
    timber = timber
)
contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber
)
twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
    timber = timber
)
twitchApiService: TwitchApiServiceInterface = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
    twitchCredentialsProvider = authRepository
)
twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService,
    seedFileReader = JsonFileReader('twitchTokensRepositorySeedFile.json')
)
twitchAnonymousUserIdProvider: TwitchAnonymousUserIdProviderInterface = TwitchAnonymousUserIdProvider()
userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchAnonymousUserIdProvider = twitchAnonymousUserIdProvider,
    twitchApiService = twitchApiService
)
websocketConnectionServer: WebsocketConnectionServerInterface = WebsocketConnectionServer(
    backgroundTaskHelper = backgroundTaskHelper,
    settingsJsonReader = JsonFileReader('websocketConnectionServer.json'),
    timber = timber
)
administratorProvider: AdministratorProviderInterface = AdministratorProvider(
    generalSettingsRepository = generalSettingsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
soundAlertJsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper(
    timber = timber
)
twitchTokensUtils: TwitchTokensUtilsInterface = TwitchTokensUtils(
    administratorProvider = administratorProvider,
    twitchTokensRepository = twitchTokensRepository
)
twitchFollowerRepository: TwitchFollowerRepositoryInterface = TwitchFollowerRepository(
    timber = timber,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository
)
timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()
usersRepository: UsersRepositoryInterface = UsersRepository(
    soundAlertJsonMapper = soundAlertJsonMapper,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)
chatLogger: ChatLoggerInterface = ChatLogger(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber
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
funtoonRepository: FuntoonRepositoryInterface = FuntoonRepository(
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
    timber = timber
)

twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface = TwitchTimeoutRemodRepository(
    backingDatabase = backingDatabase,
    timber = timber
)

twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface = TwitchTimeoutRemodHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchTimeoutRemodRepository = twitchTimeoutRemodRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

twitchTimeoutHelper: TwitchTimeoutHelperInterface = TwitchTimeoutHelper(
    timber = timber,
    twitchApiService = twitchApiService,
    twitchFollowerRepository = twitchFollowerRepository,
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    userIdsRepository = userIdsRepository
)

twitchUtils: TwitchUtilsInterface = TwitchUtils(
    backgroundTaskHelper = backgroundTaskHelper,
    generalSettingsRepository = generalSettingsRepository,
    sentMessageLogger = sentMessageLogger,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber
)

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber
)

googleJwtBuilder: GoogleJwtBuilderInterface = GoogleJwtBuilder(
    googleCloudCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper
)

googleApiService: GoogleApiServiceInterface = GoogleApiService(
    googleApiAccessTokenStorage = googleApiAccessTokenStorage,
    googleCloudProjectCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    googleJwtBuilder = googleJwtBuilder,
    networkClientProvider = networkClientProvider,
    timber = timber
)

twitchWebsocketClient: Optional[TwitchWebsocketClientInterface] = None
if generalSettingsSnapshot.isEventSubEnabled():
    twitchWebsocketClient = TwitchWebsocketClient(
        backgroundTaskHelper = backgroundTaskHelper,
        timber = timber,
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

channelPointSoundHelper: ChannelPointSoundHelperInterface | None = ChannelPointSoundHelper(
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber
)

soundPlayerManager: SoundPlayerManagerInterface | None = VlcSoundPlayerManager(
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
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
    timber = timber
)

decTalkManager: DecTalkManager | None = DecTalkManager(
    decTalkFileManager = DecTalkFileManager(
        backgroundTaskHelper = backgroundTaskHelper,
        timber = timber
    ),
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

googleTtsManager: GoogleTtsManager | None = GoogleTtsManager(
    googleApiService = googleApiService,
    googleTtsFileManager = googleTtsFileManager,
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

anivUserIdProvider: AnivUserIdProviderInterface = AnivUserIdProvider()

mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None = MostRecentAnivMessageRepository(
    backingDatabase = backingDatabase,
    timber = timber
)

mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None = None
if mostRecentAnivMessageRepository is not None:
    mostRecentAnivMessageTimeoutHelper = MostRecentAnivMessageTimeoutHelper(
        anivUserIdProvider = anivUserIdProvider,
        mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
        timber = timber,
        twitchApiService = twitchApiService,
        twitchTimeoutHelper = twitchTimeoutHelper,
        twitchTokensRepository = twitchTokensRepository
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


#########################################
## Chat Actions initialization section ##
#########################################

supStreamerChatAction: AbsChatAction | None = None
if streamAlertsManager is not None:
    supStreamerChatAction = SupStreamerChatAction(
        streamAlertsManager = streamAlertsManager,
        timber = timber
    )

chatActionsManager: ChatActionsManagerInterface = ChatActionsManager(
    anivCheckChatAction = None,
    catJamChatAction = None,
    chatLoggerChatAction = None,
    deerForceChatAction = None,
    generalSettingsRepository = generalSettingsRepository,
    mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    persistAllUsersChatAction = PersistAllUsersChatAction(
        generalSettingsRepository = generalSettingsRepository,
        userIdsRepository = userIdsRepository
    ),
    recurringActionsWizardChatAction = None,
    schubertWalkChatAction = None,
    supStreamerChatAction = supStreamerChatAction,
    timber = timber,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)


##########################################
## Cheer Actions initialization section ##
##########################################

cheerActionIdGenerator: CheerActionIdGeneratorInterface = CheerActionIdGenerator()

cheerActionsRepository: CheerActionsRepositoryInterface = CheerActionsRepository(
    backingDatabase = backingDatabase,
    cheerActionIdGenerator = cheerActionIdGenerator,
    timber = timber
)

cheerActionHelper: CheerActionHelperInterface = CheerActionHelper(
    cheerActionsRepository = cheerActionsRepository,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchFollowerRepository = twitchFollowerRepository,
    twitchHandleProvider = authRepository,
    twitchTimeoutHelper = twitchTimeoutHelper,
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    twitchTokensRepository = twitchTokensRepository,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository
)


##############################################
## Dependency Holder initialization section ##
##############################################

dependencyHolder = DependencyHolderBuilder(
    administratorProvider = administratorProvider,
    backgroundTaskHelper = backgroundTaskHelper,
    chatLogger = chatLogger,
    generalSettingsRepository = generalSettingsRepository,
    sentMessageLogger = sentMessageLogger,
    timber = timber,
    twitchUtils = twitchUtils
)\
    .build()


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    additionalTriviaAnswersRepository = None,
    administratorProvider = administratorProvider,
    authRepository = authRepository,
    backgroundTaskHelper = backgroundTaskHelper,
    bannedTriviaGameControllersRepository = None,
    bannedWordsRepository = bannedWordsRepository,
    channelJoinHelper = ChannelJoinHelper(
        backgroundTaskHelper = backgroundTaskHelper,
        verified = True,
        timber = timber,
        usersRepository = usersRepository
    ),
    channelPointSoundHelper = channelPointSoundHelper,
    chatActionsManager = chatActionsManager,
    chatLogger = chatLogger,
    cheerActionHelper = cheerActionHelper,
    cheerActionIdGenerator = cheerActionIdGenerator,
    cheerActionsRepository = cheerActionsRepository,
    cutenessRepository = None,
    cutenessUtils = None,
    dependencyHolder = dependencyHolder,
    funtoonRepository = funtoonRepository,
    funtoonTokensRepository = funtoonTokensRepository,
    generalSettingsRepository = generalSettingsRepository,
    jishoHelper = JishoHelper(
        networkClientProvider = networkClientProvider,
        timber = timber
    ),
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    languagesRepository = languagesRepository,
    locationsRepository = locationsRepository,
    modifyUserDataHelper = ModifyUserDataHelper(
        timber = timber
    ),
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
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    starWarsQuotesRepository = None,
    streamAlertsManager = streamAlertsManager,
    timber = timber,
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
    twitchConfiguration = twitchConfiguration,
    twitchFollowerRepository = twitchFollowerRepository,
    twitchPredictionWebsocketUtils = TwitchPredictionWebsocketUtils(),
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    twitchTokensRepository = twitchTokensRepository,
    twitchTokensUtils = twitchTokensUtils,
    twitchUtils = twitchUtils,
    twitchWebsocketClient = twitchWebsocketClient,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    weatherRepository = None,
    websocketConnectionServer = websocketConnectionServer,
    wordOfTheDayRepository = None
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
