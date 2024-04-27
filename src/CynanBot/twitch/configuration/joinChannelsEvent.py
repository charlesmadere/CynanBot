from CynanBot.twitch.configuration.absChannelJoinEvent import \
    AbsChannelJoinEvent
from CynanBot.twitch.configuration.channelJoinEventType import \
    ChannelJoinEventType


class JoinChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, channels: list[str]):
        if not isinstance(channels, list) or len(channels) == 0:
            raise TypeError(f'channels argument is malformed: \"{channels}\"')

        self.__channels: list[str] = channels

    def getChannels(self) -> list[str]:
        return self.__channels

    def getEventType(self) -> ChannelJoinEventType:
        return ChannelJoinEventType.JOIN
