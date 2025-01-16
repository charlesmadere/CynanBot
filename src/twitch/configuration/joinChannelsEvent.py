from .absChannelJoinEvent import AbsChannelJoinEvent
from .channelJoinEventType import ChannelJoinEventType


class JoinChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, channels: list[str]):
        if not isinstance(channels, list) or len(channels) == 0:
            raise TypeError(f'channels argument is malformed: \"{channels}\"')

        self.__channels: list[str] = channels

    @property
    def eventType(self) -> ChannelJoinEventType:
        return ChannelJoinEventType.JOIN

    def getChannels(self) -> list[str]:
        return self.__channels
