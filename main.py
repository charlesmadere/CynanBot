from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from cynanBot import CynanBot
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository

authHelper = AuthHelper()
channelIdsRepository = ChannelIdsRepository()
usersRepository = UsersRepository()
userTokensRepository = UserTokensRepository()

cynanBot = CynanBot(
    authHelper = authHelper,
    channelIdsRepository = channelIdsRepository,
    usersRepository = usersRepository,
    userTokensRepository = userTokensRepository
)

print("Starting CynanBot...")
cynanBot.run()
