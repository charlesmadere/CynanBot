from analogueStoreRepository import AnalogueStoreRepository
from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from cynanBot import CynanBot
from timeZoneRepository import TimeZoneRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from wordOfTheDayRepository import WordOfTheDayRepository

analogueStoreRepository = AnalogueStoreRepository()
authHelper = AuthHelper()
channelIdsRepository = ChannelIdsRepository()
timeZoneRepository = TimeZoneRepository()
usersRepository = UsersRepository(timeZoneRepository = timeZoneRepository)
userTokensRepository = UserTokensRepository()
wordOfTheDayRepository = WordOfTheDayRepository()

cynanBot = CynanBot(
    analogueStoreRepository = analogueStoreRepository,
    authHelper = authHelper,
    channelIdsRepository = channelIdsRepository,
    usersRepository = usersRepository,
    userTokensRepository = userTokensRepository,
    wordOfTheDayRepository = wordOfTheDayRepository
)

print("Starting CynanBot...")
cynanBot.run()
