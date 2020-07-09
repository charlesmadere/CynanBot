from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
from cynanBot import CynanBot

channelIdsRepository = ChannelIdsRepository()
authHelper = AuthHelper(channelIdsRepository = channelIdsRepository)
cynanBot = CynanBot(authHelper = authHelper)

print("Starting CynanBot...")
cynanBot.run()
