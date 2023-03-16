from twitch.twitchMessageableType import TwitchMessageableType


class TwitchMessageable():

    def getTwitchChannelName(self) -> str:
        pass

    def getTwitchMessageableType(self) -> TwitchMessageableType:
        pass

    async def send(self, message: str):
        pass
