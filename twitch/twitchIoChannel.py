from twitchio.channel import Channel

from twitch.twitchChannel import TwitchChannel
from twitch.twitchChannelType import TwitchChannelType
from twitch.twitchMessageable import TwitchMessageable


class TwitchIoChannel(TwitchChannel, TwitchMessageable):

    def __init__(self, channel: Channel):
        if not isinstance(channel, Channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')

        self.__channel: Channel = channel

    def getTwitchChannelName(self) -> str:
        return self.__channel.name

    def getTwitchChannelType(self) -> TwitchChannelType:
        return TwitchChannelType.TWITCHIO

    async def send(self, message: str):
        await self.__channel.send(message)
