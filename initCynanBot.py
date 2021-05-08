import locale

from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.funtoonRepository import FuntoonRepository
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
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
from generalSettingsRepository import GeneralSettingsRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository


locale.setlocale(locale.LC_ALL, 'en_US.utf8')

nonceRepository = NonceRepository()
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

cynanBot = CynanBot(
    analogueStoreRepository = AnalogueStoreRepository(),
    authHelper = authHelper,
    cutenessRepository = cutenessRepository,
    enEsDictionary = EnEsDictionary(
        merriamWebsterApiKey = authHelper.requireMerriamWebsterApiKey()
    ),
    funtoonRepository = FuntoonRepository(),
    jishoHelper = JishoHelper(),
    jokesRepository = JokesRepository(),
    generalSettingsRepository = GeneralSettingsRepository(),
    locationsRepository = LocationsRepository(
        timeZoneRepository = timeZoneRepository
    ),
    nonceRepository = nonceRepository,
    pokepediaRepository = PokepediaRepository(),
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    tamaleGuyRepository = TamaleGuyRepository(),
    triviaGameRepository = TriviaGameRepository(TriviaRepository()),
    twitchTokensRepository = TwitchTokensRepository(),
    userIdsRepository = UserIdsRepository(
        backingDatabase = backingDatabase
    ),
    usersRepository = UsersRepository(
        timeZoneRepository = timeZoneRepository
    ),
    weatherRepository = WeatherRepository(
        iqAirApiKey = authHelper.requireIqAirApiKey(),
        oneWeatherApiKey = authHelper.requireOneWeatherApiKey()
    ),
    wordOfTheDayRepository = WordOfTheDayRepository()
)

print('Starting CynanBot...')
cynanBot.run()
