from cynanBot import CynanBot
from secrets import TWITCH_AUTH_KEY
from secrets import TWITCH_CLIENT_ID

print("CynanBot is starting...")

cynanBot = CynanBot(
    ircToken = TWITCH_AUTH_KEY,
    clientId = TWITCH_CLIENT_ID,
    initialChannels = [ "smCharles" ]
)

cynanBot.run()
