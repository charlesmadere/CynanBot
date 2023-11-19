import asyncio
import locale
import logging
from typing import Optional

from administratorProvider import AdministratorProvider
from authRepository import AuthRepository
from cynanBot import CynanBot
from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.contentScanner.bannedWordsRepository import \
    BannedWordsRepository
from CynanBotCommon.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBotCommon.contentScanner.contentScanner import ContentScanner
from CynanBotCommon.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBotCommon.emojiHelper.emojiHelper import EmojiHelper
from CynanBotCommon.emojiHelper.emojiHelperInterface import \
    EmojiHelperInterface
from CynanBotCommon.emojiHelper.emojiRepository import EmojiRepository
from CynanBotCommon.emojiHelper.emojiRepositoryInterface import \
    EmojiRepositoryInterface
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.funtoon.funtoonRepositoryInterface import \
    FuntoonRepositoryInterface
from CynanBotCommon.funtoon.funtoonTokensRepository import \
    FuntoonTokensRepository
from CynanBotCommon.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBotCommon.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBotCommon.network.networkClientProvider import NetworkClientProvider
from CynanBotCommon.network.networkClientType import NetworkClientType
from CynanBotCommon.network.requestsClientProvider import \
    RequestsClientProvider
from CynanBotCommon.sentMessageLogger.sentMessageLogger import \
    SentMessageLogger
from CynanBotCommon.storage.backingDatabase import BackingDatabase
from CynanBotCommon.storage.backingPsqlDatabase import BackingPsqlDatabase
from CynanBotCommon.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBotCommon.storage.databaseType import DatabaseType
from CynanBotCommon.storage.jsonFileReader import JsonFileReader
from CynanBotCommon.storage.linesFileReader import LinesFileReader
from CynanBotCommon.storage.psqlCredentialsProvider import \
    PsqlCredentialsProvider
from CynanBotCommon.systemCommandHelper.systemCommandHelper import \
    SystemCommandHelper
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.tts.decTalk.decTalkCommandBuilder import \
    DecTalkCommandBuilder
from CynanBotCommon.tts.decTalk.decTalkFileManager import DecTalkFileManager
from CynanBotCommon.tts.decTalk.decTalkManager import DecTalkManager
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.tts.ttsSettingsRepository import TtsSettingsRepository
from CynanBotCommon.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface
from CynanBotCommon.twitch.isLiveOnTwitchRepository import \
    IsLiveOnTwitchRepository
from CynanBotCommon.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBotCommon.twitch.twitchApiService import TwitchApiService
from CynanBotCommon.twitch.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.twitch.websocket.twitchWebsocketAllowedUsersRepository import \
    TwitchWebsocketAllowedUsersRepository
from CynanBotCommon.twitch.websocket.twitchWebsocketClient import \
    TwitchWebsocketClient
from CynanBotCommon.twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from CynanBotCommon.twitch.websocket.twitchWebsocketJsonMapper import \
    TwitchWebsocketJsonMapper
from CynanBotCommon.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository
from twitch.channelJoinHelper import ChannelJoinHelper
from twitch.twitchConfiguration import TwitchConfiguration
from twitch.twitchIoConfiguration import TwitchIoConfiguration
from twitch.twitchUtils import TwitchUtils
from users.modifyUserDataHelper import ModifyUserDataHelper
from users.usersRepository import UsersRepository

# Uncomment this chunk to turn on extra extra debug logging
# logging.basicConfig(
#     filename = 'generalLogging.log',
#     level = logging.DEBUG
# )


locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Misc initialization section ##
#################################

eventLoop = asyncio.get_event_loop()
backgroundTaskHelper = BackgroundTaskHelper(eventLoop = eventLoop)
timber: TimberInterface = Timber(backgroundTaskHelper = backgroundTaskHelper)

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonFileReader('generalSettingsRepository.json')
)

generalSettingsSnapshot = generalSettingsRepository.getAll()

backingDatabase: BackingDatabase = None
if generalSettingsSnapshot.requireDatabaseType() is DatabaseType.POSTGRESQL:
    backingDatabase: BackingDatabase = BackingPsqlDatabase(
        eventLoop = eventLoop,
        psqlCredentialsProvider = PsqlCredentialsProvider(
            credentialsJsonReader = JsonFileReader('CynanBotCommon/storage/psqlCredentials.json')
        )
    )
elif generalSettingsSnapshot.requireDatabaseType() is DatabaseType.SQLITE:
    backingDatabase: BackingDatabase = BackingSqliteDatabase(
        eventLoop = eventLoop
    )
else:
    raise RuntimeError(f'Unknown/misconfigured database type: \"{generalSettingsSnapshot.requireDatabaseType()}\"')

networkClientProvider: NetworkClientProvider = None
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
    bannedWordsLinesReader = LinesFileReader('CynanBotCommon/contentScanner/bannedWords.txt'),
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
    seedFileReader = JsonFileReader('CynanBotCommon/twitch/twitchTokensRepositorySeedFile.json')
)
userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService
)
administratorProvider: AdministratorProviderInterface = AdministratorProvider(
    generalSettingsRepository = generalSettingsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
timeZoneRepository = TimeZoneRepository()
usersRepository: UsersRepositoryInterface = UsersRepository(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)
emojiRepository: EmojiRepositoryInterface = EmojiRepository(
    emojiJsonReader = JsonFileReader('CynanBotCommon/emojiHelper/emojiRepository.json'),
    timber = timber
)
emojiHelper: EmojiHelperInterface = EmojiHelper(
    emojiRepository = emojiRepository
)
funtoonTokensRepository: FuntoonTokensRepositoryInterface = FuntoonTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    seedFileReader = JsonFileReader('CynanBotCommon/funtoon/funtoonTokensRepositorySeedFile.json')
)
funtoonRepository: FuntoonRepositoryInterface = FuntoonRepository(
    funtoonTokensRepository = funtoonTokensRepository,
    networkClientProvider = networkClientProvider,
    timber = timber
)
isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = IsLiveOnTwitchRepository(
    administratorProvider = administratorProvider,
    twitchApiService = twitchApiService,
    twitchTokensRepository = twitchTokensRepository
)
languagesRepository = LanguagesRepository()
locationsRepository: LocationsRepositoryInterface = LocationsRepository(
    locationsJsonReader = JsonFileReader('CynanBotCommon/location/locationsRepository.json'),
    timeZoneRepository = timeZoneRepository
)
twitchConfiguration: TwitchConfiguration = TwitchIoConfiguration(
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
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
        twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
        subscriptionTypes = { WebsocketSubscriptionType.CHEER, WebsocketSubscriptionType.SUBSCRIBE, \
            WebsocketSubscriptionType.SUBSCRIPTION_GIFT, WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE }
    )


################################
## TTS initialization section ##
################################

ttsManager: Optional[TtsManagerInterface] = None

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    settingsJsonReader = JsonFileReader('CynanBotCommon/tts/ttsSettingsRepository.json')
)

if generalSettingsSnapshot.isTtsEnabled():
    ttsManager = DecTalkManager(
        backgroundTaskHelper = backgroundTaskHelper,
        decTalkFileManager = DecTalkFileManager(
            backgroundTaskHelper = backgroundTaskHelper,
            timber = timber
        ),
        ttsCommandBuilder = DecTalkCommandBuilder(
            contentScanner = contentScanner,
            emojiHelper = emojiHelper,
            timber = timber,
            ttsSettingsRepository = ttsSettingsRepository
        ),
        systemCommandHelper = SystemCommandHelper(
            timber = timber
        ),
        timber = timber,
        ttsSettingsRepository = ttsSettingsRepository
    )


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
    chatLogger = None,
    cheerActionHelper = None,
    cheerActionIdGenerator = None,
    cheerActionsRepository = None,
    cutenessRepository = None,
    cutenessUtils = None,
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
    openTriviaDatabaseTriviaQuestionRepository = None,
    pokepediaRepository = None,
    recurringActionsMachine = None,
    recurringActionsRepository = None,
    shinyTriviaOccurencesRepository = None,
    starWarsQuotesRepository = None,
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
    triviaRepository = None,
    triviaScoreRepository = None,
    triviaSettingsRepository = None,
    triviaUtils = None,
    ttsManager = ttsManager,
    ttsSettingsRepository = ttsSettingsRepository,
    twitchApiService = twitchApiService,
    twitchConfiguration = twitchConfiguration,
    twitchTokensRepository = twitchTokensRepository,
    twitchUtils = TwitchUtils(
        backgroundTaskHelper = backgroundTaskHelper,
        sentMessageLogger = SentMessageLogger(
            backgroundTaskHelper = backgroundTaskHelper
        ),
        timber = timber
    ),
    twitchWebsocketClient = twitchWebsocketClient,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    weatherRepository = None,
    wordOfTheDayRepository = None
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
