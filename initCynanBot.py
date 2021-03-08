import locale

from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.enEsDictionary import EnEsDictionary
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.locationsRepository import LocationsRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.pokepediaRepository import PokepediaRepository
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.triviaRepository import TriviaRepository
from CynanBotCommon.weatherRepository import WeatherRepository
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository


locale.setlocale(locale.LC_ALL, 'en_US.utf8')

nonceRepository = NonceRepository()
authHelper = AuthHelper(
    nonceRepository = nonceRepository
)
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
        merriamWebsterApiKey = authHelper.getMerriamWebsterApiKey()
    ),
    jishoHelper = JishoHelper(),
    jokesRepository = JokesRepository(),
    locationsRepository = LocationsRepository(
        timeZoneRepository = timeZoneRepository
    ),
    nonceRepository = nonceRepository,
    pokepediaRepository = PokepediaRepository(),
    triviaRepository = TriviaRepository(),
    userIdsRepository = UserIdsRepository(
        backingDatabase = backingDatabase
    ),
    usersRepository = UsersRepository(
        timeZoneRepository = timeZoneRepository
    ),
    userTokensRepository = UserTokensRepository(),
    weatherRepository = WeatherRepository(
        iqAirApiKey = authHelper.getIqAirApiKey(),
        oneWeatherApiKey = authHelper.getOneWeatherApiKey()
    ),
    wordOfTheDayRepository = WordOfTheDayRepository()
)

print('Starting CynanBot...')
cynanBot.run()
