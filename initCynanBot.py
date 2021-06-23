import locale
from datetime import timedelta

from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.languagesRepository import LanguagesRepository
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWarsQuotesRepository import StarWarsQuotesRepository
from CynanBotCommon.tamaleGuyRepository import TamaleGuyRepository
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.triviaGameRepository import TriviaGameRepository
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.weatherRepository import WeatherRepository
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
timeZoneRepository = TimeZoneRepository()
triviaRepository = TriviaRepository(
    cacheTimeDelta = timedelta(seconds = 1)
)

enEsDictionary = None
if authHelper.hasMerriamWebsterApiKey():
    enEsDictionary = EnEsDictionary(
        merriamWebsterApiKey = authHelper.requireMerriamWebsterApiKey()
    )

weatherRepository = None
if authHelper.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        oneWeatherApiKey = authHelper.requireOneWeatherApiKey()
    )

cynanBot = CynanBot(
    analogueStoreRepository = AnalogueStoreRepository(),
    authHelper = authHelper,
    cutenessRepository = cutenessRepository,
    doubleCutenessHelper = DoubleCutenessHelper(),
    enEsDictionary = enEsDictionary,
    funtoonRepository = FuntoonRepository(),
    generalSettingsRepository = GeneralSettingsRepository(),
    jishoHelper = JishoHelper(),
    jokesRepository = JokesRepository(),
    languagesRepository = LanguagesRepository(),
    locationsRepository = LocationsRepository(
        timeZoneRepository = timeZoneRepository
    ),
    nonceRepository = NonceRepository(),
    pokepediaRepository = PokepediaRepository(),
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    tamaleGuyRepository = TamaleGuyRepository(),
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
