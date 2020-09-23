from analogueStoreRepository import AnalogueStoreRepository
from authHelper import AuthHelper
from backingDatabase import BackingDatabase
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from jishoHelper import JishoHelper
from timeZoneRepository import TimeZoneRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from wordOfTheDayRepository import WordOfTheDayRepository

analogueStoreRepository = AnalogueStoreRepository()
authHelper = AuthHelper()
backingDatabase = BackingDatabase()
jishoHelper = JishoHelper()
userIdsRepository = UserIdsRepository(backingDatabase = backingDatabase)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    leaderboardSize = 10,
    userIdsRepository = userIdsRepository
)
timeZoneRepository = TimeZoneRepository()
usersRepository = UsersRepository(timeZoneRepository = timeZoneRepository)
userTokensRepository = UserTokensRepository()
wordOfTheDayRepository = WordOfTheDayRepository()

cynanBot = CynanBot(
    analogueStoreRepository = analogueStoreRepository,
    authHelper = authHelper,
    cutenessRepository = cutenessRepository,
    jishoHelper = jishoHelper,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    userTokensRepository = userTokensRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
)

print("Starting CynanBot...")
cynanBot.run()
