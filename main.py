from analogueStoreRepository import AnalogueStoreRepository
from authHelper import AuthHelper
from backingDatabase import BackingDatabase
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from jishoHelper import JishoHelper
import locale
from locationsRepository import LocationsRepository
from timeZoneRepository import TimeZoneRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from weatherRepository import WeatherRepository
from wordOfTheDayRepository import WordOfTheDayRepository

locale.setlocale(locale.LC_ALL, 'en_US.utf8')

analogueStoreRepository = AnalogueStoreRepository()
authHelper = AuthHelper()
backingDatabase = BackingDatabase()
jishoHelper = JishoHelper()
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
locationsRepository = LocationsRepository(
    timeZoneRepository = timeZoneRepository
)
usersRepository = UsersRepository(
    timeZoneRepository = timeZoneRepository
)
userTokensRepository = UserTokensRepository()
weatherRepository = WeatherRepository(
    authHelper = authHelper
)
wordOfTheDayRepository = WordOfTheDayRepository()

cynanBot = CynanBot(
    analogueStoreRepository = analogueStoreRepository,
    authHelper = authHelper,
    cutenessRepository = cutenessRepository,
    jishoHelper = jishoHelper,
    locationsRepository = locationsRepository,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    userTokensRepository = userTokensRepository,
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
)

print("Starting CynanBot...")
cynanBot.run()
