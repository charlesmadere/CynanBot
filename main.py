from cynanBot import CynanBot
from secretKeys import TWITCH_CLIENT_ID
from secretKeys import TWITCH_IRC_TOKEN
from users import USERS

if TWITCH_CLIENT_ID == None or len(TWITCH_CLIENT_ID) == 0 or TWITCH_CLIENT_ID.isspace():
    raise ValueError('secretKeys.TWITCH_CLIENT_ID can\'t be empty!')
elif TWITCH_IRC_TOKEN == None or len(TWITCH_IRC_TOKEN) == 0 or TWITCH_IRC_TOKEN.isspace():
    raise ValueError('secretKeys.TWITCH_IRC_TOKEN can\'t be empty!')
elif USERS == None or len(USERS) == 0:
    raise ValueError('USERS list can\'t be empty!')

cynanBot = CynanBot(
    ircToken = TWITCH_IRC_TOKEN,
    clientId = TWITCH_CLIENT_ID,
    users = USERS
)

print("Starting CynanBot...")
cynanBot.run()
