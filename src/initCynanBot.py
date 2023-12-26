import asyncio
import locale
import logging
from typing import Optional

from CynanBot.administratorProvider import AdministratorProvider
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.authRepository import AuthRepository
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.chatActions.anivCheckChatAction import AnivCheckChatAction
from CynanBot.chatActions.catJamChatAction import CatJamChatAction
from CynanBot.chatActions.chatActionsManager import ChatActionsManager
from CynanBot.chatActions.chatActionsManagerInterface import \
    ChatActionsManagerInterface
from CynanBot.chatActions.chatLoggerChatAction import ChatLoggerChatAction
from CynanBot.chatActions.deerForceChatAction import DeerForceChatAction
from CynanBot.chatActions.persistAllUsersChatAction import \
    PersistAllUsersChatAction
from CynanBot.chatActions.schubertWalkChatAction import SchubertWalkChatAction
from CynanBot.chatLogger.chatLogger import ChatLogger
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cheerActions.cheerActionHelper import CheerActionHelper
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.cheerActions.cheerActionIdGenerator import CheerActionIdGenerator
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBot.cheerActions.cheerActionRemodHelper import CheerActionRemodHelper
from CynanBot.cheerActions.cheerActionRemodHelperInterface import \
    CheerActionRemodHelperInterface
from CynanBot.cheerActions.cheerActionRemodRepository import \
    CheerActionRemodRepository
from CynanBot.cheerActions.cheerActionRemodRepositoryInterface import \
    CheerActionRemodRepositoryInterface
from CynanBot.cheerActions.cheerActionsRepository import CheerActionsRepository
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.contentScanner.aniv.anivContentScanner import AnivContentScanner
from CynanBot.contentScanner.bannedWordsRepository import BannedWordsRepository
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.contentScanner.contentScanner import ContentScanner
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.cuteness.cutenessRepository import CutenessRepository
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.cutenessUtils import CutenessUtils
from CynanBot.cynanBot import CynanBot
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
from CynanBot.language.jishoHelper import JishoHelper
from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.translationHelper import TranslationHelper
from CynanBot.language.wordOfTheDayRepository import WordOfTheDayRepository
from CynanBot.language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
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
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.recurringActions.mostRecentRecurringActionRepository import \
    MostRecentRecurringActionRepository
from CynanBot.recurringActions.recurringActionsJsonParser import \
    RecurringActionsJsonParser
from CynanBot.recurringActions.recurringActionsMachine import \
    RecurringActionsMachine
from CynanBot.recurringActions.recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from CynanBot.recurringActions.recurringActionsRepository import \
    RecurringActionsRepository
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.sentMessageLogger.sentMessageLogger import SentMessageLogger
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepository import \
    SoundPlayerSettingsRepository
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.starWars.starWarsQuotesRepository import StarWarsQuotesRepository
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.backingPsqlDatabase import BackingPsqlDatabase
from CynanBot.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.jsonFileReader import JsonFileReader
from CynanBot.storage.linesFileReader import LinesFileReader
from CynanBot.storage.psqlCredentialsProvider import PsqlCredentialsProvider
from CynanBot.systemCommandHelper.systemCommandHelper import \
    SystemCommandHelper
from CynanBot.timber.timber import Timber
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepository import \
    AdditionalTriviaAnswersRepository
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.banned.bannedTriviaGameControllersRepository import \
    BannedTriviaGameControllersRepository
from CynanBot.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBot.trivia.banned.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBot.trivia.banned.bannedTriviaIdsRepositoryInterface import \
    BannedTriviaIdsRepositoryInterface
from CynanBot.trivia.banned.triviaBanHelper import TriviaBanHelper
from CynanBot.trivia.banned.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBot.trivia.builder.triviaGameBuilder import TriviaGameBuilder
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from CynanBot.trivia.compilers.triviaQuestionCompiler import \
    TriviaQuestionCompiler
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.gameController.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBot.trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.triviaGameGlobalControllersRepository import \
    TriviaGameGlobalControllersRepository
from CynanBot.trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from CynanBot.trivia.games.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBot.trivia.games.triviaGameStore import TriviaGameStore
from CynanBot.trivia.specialStatus.shinyTriviaHelper import ShinyTriviaHelper
from CynanBot.trivia.specialStatus.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBot.trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import \
    ShinyTriviaOccurencesRepositoryInterface
from CynanBot.trivia.specialStatus.toxicTriviaHelper import ToxicTriviaHelper
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepository import \
    ToxicTriviaOccurencesRepository
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import \
    ToxicTriviaOccurencesRepositoryInterface
from CynanBot.trivia.superTriviaCooldownHelper import SuperTriviaCooldownHelper
from CynanBot.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBot.trivia.triviaContentScanner import TriviaContentScanner
from CynanBot.trivia.triviaContentScannerInterface import \
    TriviaContentScannerInterface
from CynanBot.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBot.trivia.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from CynanBot.trivia.triviaGameMachine import TriviaGameMachine
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.trivia.triviaHistoryRepository import TriviaHistoryRepository
from CynanBot.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.jokeTriviaQuestionRepository import \
    JokeTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaRepository import \
    TriviaRepository
from CynanBot.trivia.triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from CynanBot.trivia.triviaRepositories.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from CynanBot.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBot.trivia.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from CynanBot.trivia.triviaSettingsRepository import TriviaSettingsRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaSourceInstabilityHelper import \
    TriviaSourceInstabilityHelper
from CynanBot.trivia.triviaVerifier import TriviaVerifier
from CynanBot.triviaUtils import TriviaUtils
from CynanBot.tts.decTalk.decTalkCommandBuilder import DecTalkCommandBuilder
from CynanBot.tts.decTalk.decTalkFileManager import DecTalkFileManager
from CynanBot.tts.decTalk.decTalkManager import DecTalkManager
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.tts.ttsSettingsRepository import TtsSettingsRepository
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface
from CynanBot.twitch.api.twitchApiService import TwitchApiService
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.channelJoinHelper import ChannelJoinHelper
from CynanBot.twitch.configuration.twitchConfiguration import \
    TwitchConfiguration
from CynanBot.twitch.configuration.twitchIo.twitchIoConfiguration import \
    TwitchIoConfiguration
from CynanBot.twitch.isLiveOnTwitchRepository import IsLiveOnTwitchRepository
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchTokensUtils import TwitchTokensUtils
from CynanBot.twitch.twitchTokensUtilsInterface import \
    TwitchTokensUtilsInterface
from CynanBot.twitch.twitchUtils import TwitchUtils
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
from CynanBot.weather.weatherRepository import WeatherRepository
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface

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
            credentialsJsonReader = JsonFileReader('psqlCredentials.json')
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
twitchTokensUtils: TwitchTokensUtilsInterface = TwitchTokensUtils(
    administratorProvider = administratorProvider,
    twitchTokensRepository = twitchTokensRepository
)
timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()
usersRepository: UsersRepositoryInterface = UsersRepository(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)
chatLogger: ChatLoggerInterface = ChatLogger(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber
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
languagesRepository = LanguagesRepository()
locationsRepository: LocationsRepositoryInterface = LocationsRepository(
    locationsJsonReader = JsonFileReader('locationsRepository.json'),
    timeZoneRepository = timeZoneRepository
)
mostRecentChatsRepository: MostRecentChatsRepositoryInterface = MostRecentChatsRepository(
    backingDatabase = backingDatabase,
    timber = timber
)
pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    timber = timber
)
twitchConfiguration: TwitchConfiguration = TwitchIoConfiguration(
    userIdsRepository = userIdsRepository
)
twitchUtils = TwitchUtils(
    backgroundTaskHelper = backgroundTaskHelper,
    sentMessageLogger = SentMessageLogger(
        backgroundTaskHelper = backgroundTaskHelper
    ),
    timber = timber
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

shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = ToxicTriviaOccurencesRepository(
    backingDatabase = backingDatabase
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
    triviaSettingsRepository = triviaSettingsRepository
)
triviaScoreRepository: TriviaScoreRepositoryInterface = TriviaScoreRepository(
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
        jokeTriviaJsonReader = JsonFileReader('jokeTriviaQuestionRepository.json'),
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
        triviaIdGenerator = triviaIdGenerator,
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
    triviaIdGenerator = triviaIdGenerator,
    triviaRepository = triviaRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
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

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonFileReader('soundPlayerSettingsRepository.json')
)

ttsManager: Optional[TtsManagerInterface] = None

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    settingsJsonReader = JsonFileReader('ttsSettingsRepository.json')
)

if generalSettingsSnapshot.isTtsEnabled():
    ttsManager = DecTalkManager(
        backgroundTaskHelper = backgroundTaskHelper,
        decTalkCommandBuilder = DecTalkCommandBuilder(
            contentScanner = contentScanner,
            emojiHelper = emojiHelper,
            timber = timber,
            ttsSettingsRepository = ttsSettingsRepository
        ),
        decTalkFileManager = DecTalkFileManager(
            backgroundTaskHelper = backgroundTaskHelper,
            timber = timber
        ),
        soundPlayerHelper = None,
        systemCommandHelper = SystemCommandHelper(
            timber = timber
        ),
        timber = timber,
        ttsSettingsRepository = ttsSettingsRepository
    )


#########################################
## Chat Actions initialization section ##
#########################################

chatActionsManager: ChatActionsManagerInterface = ChatActionsManager(
    anivCheckChatAction = AnivCheckChatAction(
        anivContentScanner = AnivContentScanner(
            contentScanner = contentScanner,
            timber = timber
        ),
        timber = timber,
        twitchApiService = twitchApiService,
        twitchHandleProvider = authRepository,
        twitchTokensRepository = twitchTokensRepository,
        twitchUtils = twitchUtils,
        userIdsRepository = userIdsRepository
    ),
    catJamChatAction = CatJamChatAction(
        generalSettingsRepository = generalSettingsRepository,
        timber = timber,
        twitchUtils = twitchUtils
    ),
    chatLoggerChatAction = ChatLoggerChatAction(
        chatLogger = chatLogger
    ),
    deerForceChatAction = DeerForceChatAction(
        generalSettingsRepository = generalSettingsRepository,
        timber = timber,
        twitchUtils = twitchUtils
    ),
    generalSettingsRepository = generalSettingsRepository,
    mostRecentChatsRepository = mostRecentChatsRepository,
    persistAllUsersChatAction = PersistAllUsersChatAction(
        generalSettingsRepository = generalSettingsRepository,
        userIdsRepository = userIdsRepository
    ),
    schubertWalkChatAction = SchubertWalkChatAction(
        generalSettingsRepository = generalSettingsRepository,
        timber = timber,
        twitchUtils = twitchUtils
    ),
    supStreamerChatAction = None,
    timber = timber,
    ttsManager = ttsManager,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)


##########################################
## Cheer Actions initialization section ##
##########################################

cheerActionRemodRepository: CheerActionRemodRepositoryInterface = CheerActionRemodRepository(
    backingDatabase = backingDatabase,
    timber = timber
)

cheerActionRemodHelper: CheerActionRemodHelperInterface = CheerActionRemodHelper(
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
    chatActionsManager = chatActionsManager,
    chatLogger = chatLogger,
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
    mostRecentChatsRepository = mostRecentChatsRepository,
    openTriviaDatabaseTriviaQuestionRepository = openTriviaDatabaseTriviaQuestionRepository,
    pokepediaRepository = pokepediaRepository,
    recurringActionsMachine = recurringActionsMachine,
    recurringActionsRepository = recurringActionsRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    starWarsQuotesRepository = StarWarsQuotesRepository(
        quotesJsonReader = JsonFileReader('starWarsQuotesRepository.json')
    ),
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
    triviaIdGenerator = triviaIdGenerator,
    triviaRepository = triviaRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
    triviaUtils = triviaUtils,
    ttsManager = ttsManager,
    ttsSettingsRepository = ttsSettingsRepository,
    twitchApiService = twitchApiService,
    twitchConfiguration = twitchConfiguration,
    twitchTokensRepository = twitchTokensRepository,
    twitchTokensUtils = twitchTokensUtils,
    twitchUtils = twitchUtils,
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
