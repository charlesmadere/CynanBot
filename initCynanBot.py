import asyncio
import locale
import logging
from typing import Optional

from administratorProvider import AdministratorProvider
from authRepository import AuthRepository
from cutenessUtils import CutenessUtils
from cynanBot import CynanBot
from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.cheerActions.cheerActionHelper import CheerActionHelper
from CynanBotCommon.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBotCommon.cheerActions.cheerActionIdGenerator import \
    CheerActionIdGenerator
from CynanBotCommon.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBotCommon.cheerActions.cheerActionRemodHelper import \
    CheerActionRemodHelper
from CynanBotCommon.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBotCommon.cheerActions.cheerActionRemodRepository import \
    CheerActionRemodRepository
from CynanBotCommon.cheerActions.cheerActionRemodRepositoryInterface import \
    CheerActionRemodRepositoryInterface
from CynanBotCommon.cheerActions.cheerActionsRepository import \
    CheerActionsRepository
from CynanBotCommon.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBotCommon.contentScanner.bannedWordsRepository import \
    BannedWordsRepository
from CynanBotCommon.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBotCommon.contentScanner.contentScanner import ContentScanner
from CynanBotCommon.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
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
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBotCommon.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBotCommon.network.networkClientProvider import NetworkClientProvider
from CynanBotCommon.network.networkClientType import NetworkClientType
from CynanBotCommon.network.requestsClientProvider import \
    RequestsClientProvider
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.recurringActions.mostRecentRecurringActionRepository import \
    MostRecentRecurringActionRepository
from CynanBotCommon.recurringActions.recurringActionsJsonParser import \
    RecurringActionsJsonParser
from CynanBotCommon.recurringActions.recurringActionsMachine import \
    RecurringActionsMachine
from CynanBotCommon.recurringActions.recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from CynanBotCommon.recurringActions.recurringActionsRepository import \
    RecurringActionsRepository
from CynanBotCommon.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBotCommon.sentMessageLogger.sentMessageLogger import \
    SentMessageLogger
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
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
from CynanBotCommon.trivia.additionalTriviaAnswersRepository import \
    AdditionalTriviaAnswersRepository
from CynanBotCommon.trivia.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBotCommon.trivia.bannedTriviaGameControllersRepository import \
    BannedTriviaGameControllersRepository
from CynanBotCommon.trivia.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBotCommon.trivia.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBotCommon.trivia.bannedTriviaIdsRepositoryInterface import \
    BannedTriviaIdsRepositoryInterface
from CynanBotCommon.trivia.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBotCommon.trivia.shinyTriviaHelper import ShinyTriviaHelper
from CynanBotCommon.trivia.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBotCommon.trivia.superTriviaCooldownHelper import \
    SuperTriviaCooldownHelper
from CynanBotCommon.trivia.toxicTriviaHelper import ToxicTriviaHelper
from CynanBotCommon.trivia.toxicTriviaOccurencesRepository import \
    ToxicTriviaOccurencesRepository
from CynanBotCommon.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBotCommon.trivia.triviaBanHelper import TriviaBanHelper
from CynanBotCommon.trivia.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBotCommon.trivia.triviaContentScanner import TriviaContentScanner
from CynanBotCommon.trivia.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from CynanBotCommon.trivia.triviaGameBuilder import TriviaGameBuilder
from CynanBotCommon.trivia.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBotCommon.trivia.triviaGameGlobalControllersRepository import \
    TriviaGameGlobalControllersRepository
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBotCommon.trivia.triviaGameStore import TriviaGameStore
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBotCommon.trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from CynanBotCommon.trivia.triviaRepositories.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.jokeTriviaQuestionRepository import \
    JokeTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBotCommon.trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.triviaRepository import \
    TriviaRepository
from CynanBotCommon.trivia.triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from CynanBotCommon.trivia.triviaRepositories.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBotCommon.trivia.triviaRepositories.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBotCommon.trivia.triviaSourceInstabilityHelper import \
    TriviaSourceInstabilityHelper
from CynanBotCommon.trivia.triviaVerifier import TriviaVerifier
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
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from CynanBotCommon.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository
from triviaUtils import TriviaUtils
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
cutenessRepository: CutenessRepositoryInterface = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
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
pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    timber = timber
)
twitchConfiguration: TwitchConfiguration = TwitchIoConfiguration(
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)
wordOfTheDayRepository: WordOfTheDayRepositoryInterface = WordOfTheDayRepository(
    networkClientProvider = networkClientProvider,
    timber = timber
)

authSnapshot = authRepository.getAll()

translationHelper: Optional[TranslationHelper] = None
if authSnapshot.hasDeepLAuthKey():
    translationHelper = TranslationHelper(
        languagesRepository = languagesRepository,
        networkClientProvider = networkClientProvider,
        deepLAuthKey = authSnapshot.requireDeepLAuthKey(),
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

weatherRepository: Optional[WeatherRepositoryInterface] = None
if authSnapshot.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        networkClientProvider = networkClientProvider,
        oneWeatherApiKey = authSnapshot.requireOneWeatherApiKey(),
        timber = timber
    )


###################################
## Trivia initialization section ##
###################################

shinyTriviaOccurencesRepository = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
toxicTriviaOccurencesRepository = ToxicTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
triviaAnswerCompiler = TriviaAnswerCompiler(
    timber = timber
)
triviaIdGenerator: TriviaIdGeneratorInterface = TriviaIdGenerator()
triviaQuestionCompiler = TriviaQuestionCompiler()
triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader('CynanBotCommon/trivia/triviaSettingsRepository.json')
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
    triviaSettingsRepository = triviaSettingsRepository
)
toxicTriviaHelper = ToxicTriviaHelper(
    toxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaBanHelper: TriviaBanHelperInterface = TriviaBanHelper(
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    funtoonRepository = funtoonRepository,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    contentScanner = contentScanner,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaEmoteGenerator: TriviaEmoteGeneratorInterface = TriviaEmoteGenerator(
    backingDatabase = backingDatabase,
    timber = timber
)
triviaGameBuilder: TriviaGameBuilderInterface = TriviaGameBuilder(
    triviaGameBuilderSettings = generalSettingsRepository,
    usersRepository = usersRepository
)
bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = BannedTriviaGameControllersRepository(
    administratorProvider = administratorProvider,
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaGameControllersRepository = TriviaGameControllersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaGameGlobalControllersRepository = TriviaGameGlobalControllersRepository(
    administratorProvider = administratorProvider,
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaHistoryRepository: TriviaHistoryRepositoryInterface = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaScoreRepository = TriviaScoreRepository(
    backingDatabase = backingDatabase
)
triviaUtils = TriviaUtils(
    administratorProvider = administratorProvider,
    bannedTriviaGameControllersRepository = bannedTriviaGameControllersRepository,
    timber = timber,
    triviaGameControllersRepository = triviaGameControllersRepository,
    triviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)

quizApiTriviaQuestionRepository: Optional[QuizApiTriviaQuestionRepository] = None
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
    jokeTriviaQuestionRepository = JokeTriviaQuestionRepository(
        timber = timber,
        triviaSettingsRepository = triviaSettingsRepository
    ),
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
    triviaSourceInstabilityHelper = TriviaSourceInstabilityHelper(
        timber = timber
    ),
    triviaSettingsRepository = triviaSettingsRepository,
    triviaVerifier = TriviaVerifier(
        timber = timber,
        triviaBanHelper = triviaBanHelper,
        triviaContentScanner = triviaContentScanner,
        triviaHistoryRepository = triviaHistoryRepository
    ),
    twitchHandleProvider = authRepository,
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
        triviaSettingsRepository = triviaSettingsRepository
    ),
    shinyTriviaHelper = shinyTriviaHelper,
    superTriviaCooldownHelper = SuperTriviaCooldownHelper(
        triviaSettingsRepository = triviaSettingsRepository
    ),
    timber = timber,
    toxicTriviaHelper = toxicTriviaHelper,
    triviaAnswerChecker = TriviaAnswerChecker(
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameStore = TriviaGameStore(),
    triviaRepository = triviaRepository,
    triviaScoreRepository = triviaScoreRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)


##############################################
## Recurring Actions initialization section ##
##############################################

recurringActionsRepository: RecurringActionsRepositoryInterface = RecurringActionsRepository(
    backingDatabase = backingDatabase,
    recurringActionsJsonParser = RecurringActionsJsonParser(
        languagesRepository = languagesRepository
    ),
    timber = timber
)

recurringActionsMachine: RecurringActionsMachineInterface = RecurringActionsMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    locationsRepository = locationsRepository,
    mostRecentRecurringActionRepository = MostRecentRecurringActionRepository(
        backingDatabase = backingDatabase,
        timber = timber
    ),
    recurringActionsRepository = recurringActionsRepository,
    timber = timber,
    triviaGameBuilder = triviaGameBuilder,
    triviaGameMachine = triviaGameMachine,
    usersRepository = usersRepository,
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
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


##########################################
## Cheer Actions initialization section ##
##########################################

cheerActionRemodRepository: CheerActionRemodRepositoryInterface = CheerActionRemodRepository(
    backingDatabase = backingDatabase,
    timber = timber
)

cheerActionRemodHelper: CheerActionRemodHelperInterface = CheerActionRemodHelper(
    administratorProvider = administratorProvider,
    backgroundTaskHelper = backgroundTaskHelper,
    cheerActionRemodRepository = cheerActionRemodRepository,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchTokensRepository = twitchTokensRepository
)

cheerActionIdGenerator: CheerActionIdGeneratorInterface = CheerActionIdGenerator()

cheerActionsRepository: CheerActionsRepositoryInterface = CheerActionsRepository(
    backingDatabase = backingDatabase,
    cheerActionIdGenerator = cheerActionIdGenerator,
    timber = timber
)

cheerActionHelper: CheerActionHelperInterface = CheerActionHelper(
    administratorProvider = administratorProvider,
    cheerActionRemodHelper = cheerActionRemodHelper,
    cheerActionsRepository = cheerActionsRepository,
    timber = timber,
    ttsManager = ttsManager,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    additionalTriviaAnswersRepository = additionalTriviaAnswersRepository,
    administratorProvider = administratorProvider,
    authRepository = authRepository,
    backgroundTaskHelper = backgroundTaskHelper,
    bannedTriviaGameControllersRepository = bannedTriviaGameControllersRepository,
    bannedWordsRepository = bannedWordsRepository,
    channelJoinHelper = ChannelJoinHelper(
        backgroundTaskHelper = backgroundTaskHelper,
        verified = True,
        timber = timber,
        usersRepository = usersRepository
    ),
    chatLogger = ChatLogger(
        backgroundTaskHelper = backgroundTaskHelper,
        timber = timber
    ),
    cheerActionHelper = cheerActionHelper,
    cheerActionIdGenerator = cheerActionIdGenerator,
    cheerActionRemodHelper = cheerActionRemodHelper,
    cheerActionsRepository = cheerActionsRepository,
    cutenessRepository = cutenessRepository,
    cutenessUtils = CutenessUtils(),
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
    openTriviaDatabaseTriviaQuestionRepository = openTriviaDatabaseTriviaQuestionRepository,
    pokepediaRepository = pokepediaRepository,
    recurringActionsMachine = recurringActionsMachine,
    recurringActionsRepository = recurringActionsRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    timber = timber,
    toxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository,
    translationHelper = translationHelper,
    triviaBanHelper = triviaBanHelper,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameBuilder = triviaGameBuilder,
    triviaGameControllersRepository = triviaGameControllersRepository,
    triviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository,
    triviaGameMachine = triviaGameMachine,
    triviaHistoryRepository = triviaHistoryRepository,
    triviaRepository = triviaRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
    triviaUtils = triviaUtils,
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
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
