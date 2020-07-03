from cynanBot import CynanBot
from secretKeys import TWITCH_CLIENT_ID
from secretKeys import TWITCH_IRC_TOKEN
from users import USERS

cynanBot = CynanBot(
    ircToken = TWITCH_IRC_TOKEN,
    clientId = TWITCH_CLIENT_ID,
    users = USERS
)

print("Starting CynanBot...")
cynanBot.run()
