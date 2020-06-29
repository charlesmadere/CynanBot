from cynanBot import CynanBot
from secretKeys import TWITCH_CLIENT_ID
from secretKeys import TWITCH_CLIENT_SECRET
from secretKeys import TWITCH_IRC_TOKEN
from secretKeys import TWITCH_PUB_SUB_TOKEN
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
    pubSubId = TWITCH_PUB_SUB_TOKEN,
    users = users
)

print("Starting CynanBot...")
cynanBot.run()
