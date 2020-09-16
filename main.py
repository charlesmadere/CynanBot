from analogueStoreRepository import AnalogueStoreRepository
from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from timeZoneRepository import TimeZoneRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from wordOfTheDayRepository import WordOfTheDayRepository

analogueStoreRepository = AnalogueStoreRepository()
authHelper = AuthHelper()
channelIdsRepository = ChannelIdsRepository()
cutenessRepository = CutenessRepository()
timeZoneRepository = TimeZoneRepository()
usersRepository = UsersRepository(timeZoneRepository = timeZoneRepository)
userTokensRepository = UserTokensRepository()
wordOfTheDayRepository = WordOfTheDayRepository()

cynanBot = CynanBot(
    analogueStoreRepository = analogueStoreRepository,
    authHelper = authHelper,
    channelIdsRepository = channelIdsRepository,
    cutenessRepository = cutenessRepository,
    usersRepository = usersRepository,
    userTokensRepository = userTokensRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
)

print("Starting CynanBot...")
cynanBot.run()
