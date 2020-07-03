from user import User

# The accessToken and refreshToken values in this file should be generated
# using the fetchTokens.py script. The rewardId is gathered from reading the
# Twitch pubsub API itself, so you'll need to run the actual bot first and
# inspect the incoming JSON data to determine that information.

USERS = [
    # User(
    #     twitchHandle = "Imyt",
    #     picOfTheDayFile = "/home/declan/potd.txt",
    #     accessToken = "",
    #     refreshToken = "",
    #     rewardId = ""
    # ),
    User(
        twitchHandle = "smCharles",
        picOfTheDayFile = "/home/charles/potd.txt",
        accessToken = "",
        refreshToken = "",
        rewardId = "fc83a5e8-4ff9-459b-ba98-64454964b5f8",
    )
]
