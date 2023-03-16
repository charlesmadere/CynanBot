from twitch.twitchConfigurationType import TwitchConfigurationType


class TwitchMessageable():

    def getTwitchChannelName(self) -> str:
        pass

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    async def send(self, message: str):
        pass
