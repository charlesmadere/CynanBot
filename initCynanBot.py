import locale

from authHelper import AuthHelper
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
from CynanBotCommon.trivia.localTriviaRepository import LocalTriviaRepository
from CynanBotCommon.trivia.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnection.websocketConnectionServer import \
    WebsocketConnectionServer
from generalSettingsRepository import GeneralSettingsRepository
from users.userIdsRepository import UserIdsRepository
from users.usersRepository import UsersRepository

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


timber = Timber()
authHelper = AuthHelper()
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
    localTriviaRepository = LocalTriviaRepository(),
    timber = timber,
    cacheTimeDelta = None
)
websocketConnectionServer = WebsocketConnectionServer(
    timber = timber,
    isDebugLoggingEnabled = True
)

translationHelper: TranslationHelper = None
if authHelper.hasDeepLAuthKey():
    translationHelper = TranslationHelper(
        languagesRepository = languagesRepository,
        deepLAuthKey = authHelper.requireDeepLAuthKey(),
        timber = timber
    )

weatherRepository: WeatherRepository = None
if authHelper.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        oneWeatherApiKey = authHelper.requireOneWeatherApiKey(),
        timber = timber
    )

cynanBot = CynanBot(
    analogueStoreRepository = AnalogueStoreRepository(
        timber = timber
    ),
    authHelper = authHelper,
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
