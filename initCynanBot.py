import locale

from authRepository import AuthRepository
from cuteness.cutenessRepository import CutenessRepository
from cuteness.doubleCutenessHelper import DoubleCutenessHelper
from cynanBot import CynanBot
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
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
from CynanBotCommon.trivia.generalTriviaSettingsRepository import \
    GeneralTriviaSettingsRepository
from CynanBotCommon.trivia.jokeTriviaRepository import JokeTriviaRepository
from CynanBotCommon.trivia.triviaContentScanner import TriviaContentScanner
from CynanBotCommon.trivia.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaVerifier import TriviaVerifier
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from generalSettingsRepository import GeneralSettingsRepository
from triviaUtils import TriviaUtils
from users.userIdsRepository import UserIdsRepository
from users.usersRepository import UsersRepository

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


timber = Timber()
authRepository = AuthRepository()
backingDatabase = BackingDatabase()
userIdsRepository = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber
)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)
languagesRepository = LanguagesRepository()
timeZoneRepository = TimeZoneRepository()

triviaRepository = TriviaRepository(
    generalTriviaSettingsRepository = GeneralTriviaSettingsRepository(),
    jokeTriviaRepository = JokeTriviaRepository(
        timber = timber
    ),
    timber = timber,
    triviaIdGenerator = TriviaIdGenerator(),
    triviaVerifier = TriviaVerifier(
        triviaContentScanner = TriviaContentScanner(),
        triviaHistoryRepository = TriviaHistoryRepository(
            backingDatabase = backingDatabase,
            timber = timber
        )
    ),
    quizApiKey = authRepository.getQuizApiKey(),
    cacheTimeDelta = None
)

websocketConnectionServer = WebsocketConnectionServer(
    timber = timber,
    isDebugLoggingEnabled = True
)

translationHelper: TranslationHelper = None
if authRepository.hasDeepLAuthKey():
    translationHelper = TranslationHelper(
        languagesRepository = languagesRepository,
        deepLAuthKey = authRepository.requireDeepLAuthKey(),
        timber = timber
    )

weatherRepository: WeatherRepository = None
if authRepository.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        oneWeatherApiKey = authRepository.requireOneWeatherApiKey(),
        timber = timber
    )

cynanBot = CynanBot(
    analogueStoreRepository = AnalogueStoreRepository(
        timber = timber
    ),
    authRepository = authRepository,
    chatBandManager = ChatBandManager(
        timber = timber,
        websocketConnectionServer = websocketConnectionServer
    ),
    cutenessRepository = cutenessRepository,
    doubleCutenessHelper = DoubleCutenessHelper(),
    funtoonRepository = FuntoonRepository(
        timber = timber
    ),
    generalSettingsRepository = GeneralSettingsRepository(),
    jishoHelper = JishoHelper(
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
        timber = timber
    ),
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    tamaleGuyRepository = TamaleGuyRepository(
        timber = timber
    ),
    timber = timber,
    translationHelper = translationHelper,
    triviaGameRepository = TriviaGameRepository(
        triviaRepository = triviaRepository
    ),
    triviaRepository = triviaRepository,
    triviaScoreRepository = TriviaScoreRepository(
        backingDatabase = backingDatabase
    ),
    triviaUtils = TriviaUtils(),
    twitchTokensRepository = TwitchTokensRepository(
        timber = timber
    ),
    userIdsRepository = userIdsRepository,
    usersRepository = UsersRepository(
        timeZoneRepository = timeZoneRepository
    ),
    weatherRepository = weatherRepository,
    websocketConnectionServer = websocketConnectionServer,
    wordOfTheDayRepository = WordOfTheDayRepository(
        timber = timber
    )
)

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
