from cynanBot import CynanBot
from secretKeys import TWITCH_ACCESS_TOKEN
from secretKeys import TWITCH_CLIENT_ID
from secretKeys import TWITCH_CLIENT_SECRET
from secretKeys import TWITCH_IRC_TOKEN
from secretKeys import TWITCH_REFRESH_TOKEN
from user import User

users = [
    User(
        twitchHandle = "Imyt",
        picOfTheDayFile = "/home/declan/potd.txt"
    ),
    User(
        twitchHandle = "smCharles",
        picOfTheDayFile = "/home/charles/potd.txt"
    )
]

cynanBot = CynanBot(
    ircToken = TWITCH_IRC_TOKEN,
    clientId = TWITCH_CLIENT_ID,
    clientSecret = TWITCH_CLIENT_SECRET,
    accessToken = TWITCH_ACCESS_TOKEN,
    refreshToken = TWITCH_REFRESH_TOKEN,
    users = users
)

print("Starting CynanBot...")
cynanBot.run()
