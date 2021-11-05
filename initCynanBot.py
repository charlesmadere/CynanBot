import locale

from authHelper import AuthHelper
from cuteness.cutenessRepository import CutenessRepository
from cuteness.doubleCutenessHelper import DoubleCutenessHelper
from cynanBot import CynanBot
from CynanBotCommon.analogue.analogueStoreRepository import \
    AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.localTriviaRepository import LocalTriviaRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from CynanBotCommon.websocketConnectionServer import WebsocketConnectionServer
from generalSettingsRepository import GeneralSettingsRepository
from user.userIdsRepository import UserIdsRepository
from user.usersRepository import UsersRepository


locale.setlocale(locale.LC_ALL, 'en_US.utf8')

authHelper = AuthHelper()
backingDatabase = BackingDatabase()
userIdsRepository = UserIdsRepository(
    backingDatabase = backingDatabase
)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)
languagesRepository = LanguagesRepository()
timeZoneRepository = TimeZoneRepository()
triviaRepository = TriviaRepository(
    localTriviaRepository = LocalTriviaRepository(),
    cacheTimeDelta = None
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
    triviaScoreRepository = TriviaScoreRepository(
        backingDatabase = backingDatabase
    ),
    twitchTokensRepository = TwitchTokensRepository(),
    userIdsRepository = UserIdsRepository(
        backingDatabase = backingDatabase
    ),
    usersRepository = UsersRepository(
        timeZoneRepository = timeZoneRepository
    ),
    weatherRepository = weatherRepository,
    websocketConnectionServer = websocketConnectionServer,
    wordOfTheDayRepository = WordOfTheDayRepository()
)

print('Starting CynanBot...')
cynanBot.run()
