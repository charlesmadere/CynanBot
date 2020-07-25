from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from cynanBot import CynanBot
from timeZoneRepository import TimeZoneRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository

authHelper = AuthHelper()
channelIdsRepository = ChannelIdsRepository()
timeZoneRepository = TimeZoneRepository()
usersRepository = UsersRepository(
    timeZoneRepository = timeZoneRepository
)
userTokensRepository = UserTokensRepository()

cynanBot = CynanBot(
    authHelper = authHelper,
    channelIdsRepository = channelIdsRepository,
    usersRepository = usersRepository,
    userTokensRepository = userTokensRepository
)

print("Starting CynanBot...")
cynanBot.run()
