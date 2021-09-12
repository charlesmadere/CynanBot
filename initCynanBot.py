import locale
from datetime import timedelta

from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.chatBandManager import ChatBandManager
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.languagesRepository import LanguagesRepository
from CynanBotCommon.localTriviaRepository import LocalTriviaRepository
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWarsQuotesRepository import StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.translationHelper import TranslationHelper
from CynanBotCommon.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnectionServer import WebsocketConnectionServer
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from doubleCutenessHelper import DoubleCutenessHelper
from generalSettingsRepository import GeneralSettingsRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository


locale.setlocale(locale.LC_ALL, 'en_US.utf8')

authHelper = AuthHelper()
backingDatabase = BackingDatabase()
userIdsRepository = UserIdsRepository(
    backingDatabase = backingDatabase
)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    leaderboardSize = 10,
    localLeaderboardSize = 5,
    userIdsRepository = userIdsRepository
)
languagesRepository = LanguagesRepository()
timeZoneRepository = TimeZoneRepository()
triviaRepository = TriviaRepository(
    localTriviaRepository = LocalTriviaRepository(),
    cacheTimeDelta = timedelta(seconds = 1)
)
websocketConnectionServer = WebsocketConnectionServer()

enEsDictionary: EnEsDictionary = None
if authHelper.hasMerriamWebsterApiKey():
    enEsDictionary = EnEsDictionary(
        merriamWebsterApiKey = authHelper.requireMerriamWebsterApiKey()
    )

translationHelper: TranslationHelper = None
if authHelper.hasDeepLAuthKey():
    translationHelper = TranslationHelper(
        languagesRepository = languagesRepository,
        deepLAuthKey = authHelper.requireDeepLAuthKey()
    )

weatherRepository: WeatherRepository = None
if authHelper.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        oneWeatherApiKey = authHelper.requireOneWeatherApiKey()
    )

cynanBot = CynanBot(
    analogueStoreRepository = AnalogueStoreRepository(),
    authHelper = authHelper,
    chatBandManager = ChatBandManager(
        websocketConnectionServer = websocketConnectionServer
    ),
    cutenessRepository = cutenessRepository,
    doubleCutenessHelper = DoubleCutenessHelper(),
    enEsDictionary = enEsDictionary,
    funtoonRepository = FuntoonRepository(),
    generalSettingsRepository = GeneralSettingsRepository(),
    jishoHelper = JishoHelper(),
    jokesRepository = JokesRepository(),
    languagesRepository = languagesRepository,
    locationsRepository = LocationsRepository(
        timeZoneRepository = timeZoneRepository
    ),
    nonceRepository = NonceRepository(),
    pokepediaRepository = PokepediaRepository(),
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    tamaleGuyRepository = TamaleGuyRepository(),
    translationHelper = translationHelper,
    triviaGameRepository = TriviaGameRepository(
        triviaRepository = triviaRepository
    ),
    triviaRepository = triviaRepository,
    twitchTokensRepository = TwitchTokensRepository(),
    userIdsRepository = UserIdsRepository(
        backingDatabase = backingDatabase
    ),
    usersRepository = UsersRepository(
        timeZoneRepository = timeZoneRepository
    ),
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = WordOfTheDayRepository()
)

print('Starting CynanBot...')
cynanBot.run()
