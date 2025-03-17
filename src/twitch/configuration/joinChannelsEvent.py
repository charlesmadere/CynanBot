from typing import Any

from frozenlist import FrozenList

from .absChannelJoinEvent import AbsChannelJoinEvent
from .channelJoinEventType import ChannelJoinEventType


class JoinChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, channels: FrozenList[str]):
        if not isinstance(channels, FrozenList) or len(channels) == 0:
            raise TypeError(f'channels argument is malformed: \"{channels}\"')

        self.__channels: FrozenList[str] = channels

    @property
    def channels(self) -> list[str]:
        return list(self.__channels)

    @property
    def eventType(self) -> ChannelJoinEventType:
        return ChannelJoinEventType.JOIN

    def toDictionary(self) -> dict[str, Any]:
        return {
            'channels': self.__channels,
            'eventType': self.eventType
        }
