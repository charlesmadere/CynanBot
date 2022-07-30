import asyncio
import locale

import aiohttp

from authRepository import AuthRepository
from cutenessUtils import CutenessUtils
from cynanBot import CynanBot
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.cuteness.doubleCutenessHelper import DoubleCutenessHelper
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.trivia.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBotCommon.trivia.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBotCommon.trivia.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBotCommon.trivia.jokeTriviaQuestionRepository import \
    JokeTriviaQuestionRepository
from CynanBotCommon.trivia.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBotCommon.trivia.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBotCommon.trivia.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBotCommon.trivia.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBotCommon.trivia.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBotCommon.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBotCommon.trivia.triviaContentScanner import TriviaContentScanner
from CynanBotCommon.trivia.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaGameStore import TriviaGameStore
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.trivia.triviaVerifier import TriviaVerifier
from CynanBotCommon.trivia.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBotCommon.trivia.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.userIdsRepository import UserIdsRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from generalSettingsRepository import GeneralSettingsRepository
from triviaUtils import TriviaUtils
from users.usersRepository import UsersRepository

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Misc initialization section ##
#################################

authRepository = AuthRepository()
backingDatabase = BackingDatabase()
clientSession = aiohttp.ClientSession(
    cookie_jar = aiohttp.DummyCookieJar(),
    timeout = aiohttp.ClientTimeout(total = 8)
)
eventLoop = asyncio.get_event_loop()
timber = Timber(
    eventLoop = eventLoop
)

userIdsRepository = UserIdsRepository(
    clientSession = clientSession,
    backingDatabase = backingDatabase,
    timber = timber
)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)
languagesRepository = LanguagesRepository()
timeZoneRepository = TimeZoneRepository()

websocketConnectionServer = WebsocketConnectionServer(
    eventLoop = eventLoop,
    timber = timber
)

authSnapshot = authRepository.getAll()

translationHelper: TranslationHelper = None
if authSnapshot.hasDeepLAuthKey():
    translationHelper = TranslationHelper(
        clientSession = clientSession,
        languagesRepository = languagesRepository,
        deepLAuthKey = authSnapshot.requireDeepLAuthKey(),
        timber = timber
    )

weatherRepository: WeatherRepository = None
if authSnapshot.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        clientSession = clientSession,
        oneWeatherApiKey = authSnapshot.requireOneWeatherApiKey(),
        timber = timber
    )


###################################
## Trivia initialization section ##
###################################

triviaAnswerCompiler = TriviaAnswerCompiler()
triviaIdGenerator = TriviaIdGenerator()
triviaQuestionCompiler = TriviaQuestionCompiler()
triviaSettingsRepository = TriviaSettingsRepository()
bannedTriviaIdsRepository = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaContentScanner = TriviaContentScanner(
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaEmoteGenerator = TriviaEmoteGenerator(
    backingDatabase = backingDatabase
)
triviaHistoryRepository = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaScoreRepository = TriviaScoreRepository(
    backingDatabase = backingDatabase
)

quizApiTriviaQuestionRepository: QuizApiTriviaQuestionRepository = None
if authSnapshot.hasQuizApiKey():
    quizApiTriviaQuestionRepository = QuizApiTriviaQuestionRepository(
        clientSession = clientSession,
        quizApiKey = authSnapshot.requireQuizApiKey(),
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

triviaRepository = TriviaRepository(
    bongoTriviaQuestionRepository = BongoTriviaQuestionRepository(
        clientSession = clientSession,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
        clientSession = clientSession,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    jokeTriviaQuestionRepository = JokeTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    jServiceTriviaQuestionRepository = JServiceTriviaQuestionRepository(
        clientSession = clientSession,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    lotrTriviaQuestionsRepository = LotrTriviaQuestionRepository(
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    millionaireTriviaQuestionRepository = MillionaireTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
        clientSession = clientSession,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    quizApiTriviaQuestionRepository = quizApiTriviaQuestionRepository,
    timber = timber,
    triviaDatabaseTriviaQuestionRepository = TriviaDatabaseTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaSettingsRepository = triviaSettingsRepository,
    triviaVerifier = TriviaVerifier(
        bannedTriviaIdsRepository = bannedTriviaIdsRepository,
        timber = timber,
        triviaContentScanner = triviaContentScanner,
        triviaHistoryRepository = triviaHistoryRepository
    ),
    willFryTriviaQuestionRepository = WillFryTriviaQuestionRepository(
        clientSession = clientSession,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    wwtbamTriviaQuestionRepository = WwtbamTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    )
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    analogueStoreRepository = AnalogueStoreRepository(
        clientSession = clientSession,
        timber = timber
    ),
    authRepository = authRepository,
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    chatBandManager = ChatBandManager(
        timber = timber,
        websocketConnectionServer = websocketConnectionServer
    ),
    chatLogger = ChatLogger(
        eventLoop = eventLoop,
    ),
    cutenessRepository = cutenessRepository,
    cutenessUtils = CutenessUtils(),
    doubleCutenessHelper = DoubleCutenessHelper(),
    funtoonRepository = FuntoonRepository(
        clientSession = clientSession,
        timber = timber
    ),
    generalSettingsRepository = GeneralSettingsRepository(),
    jishoHelper = JishoHelper(
        clientSession = clientSession,
        timber = timber
    ),
    languagesRepository = languagesRepository,
    locationsRepository = LocationsRepository(
        timeZoneRepository = timeZoneRepository
    ),
    nonceRepository = NonceRepository(
        timber = timber
    ),
    pokepediaRepository = PokepediaRepository(
        clientSession = clientSession,
        timber = timber
    ),
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    tamaleGuyRepository = TamaleGuyRepository(
        clientSession = clientSession,
        timber = timber
    ),
    timber = timber,
    translationHelper = translationHelper,
    triviaContentScanner = triviaContentScanner,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameMachine = TriviaGameMachine(
        eventLoop = eventLoop,
        timber = timber,
        triviaAnswerChecker = TriviaAnswerChecker(
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        triviaGameStore = TriviaGameStore(),
        triviaRepository = triviaRepository,
        triviaScoreRepository = triviaScoreRepository
    ),
    triviaHistoryRepository = triviaHistoryRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
    triviaUtils = TriviaUtils(),
    twitchTokensRepository = TwitchTokensRepository(
        clientSession = clientSession,
        timber = timber
    ),
    userIdsRepository = userIdsRepository,
    usersRepository = UsersRepository(
        timeZoneRepository = timeZoneRepository
    ),
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = WordOfTheDayRepository(
        clientSession = clientSession,
        timber = timber
    )
)

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
