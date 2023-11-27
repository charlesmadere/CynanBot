from twitchio.channel import Channel

from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable


class TwitchIoChannel(TwitchChannel, TwitchMessageable):

    def __init__(self, channel: Channel):
        if not isinstance(channel, Channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')

        self.__channel: Channel = channel

    def getTwitchChannelName(self) -> str:
        return self.__channel.name

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    async def send(self, message: str):
        await self.__channel.send(message)

    def __str__(self) -> str:
        return self.getTwitchChannelName()
