from typing import Any

from frozenlist import FrozenList

from .absChannelJoinEvent import AbsChannelJoinEvent
from .channelJoinEventType import ChannelJoinEventType


class FinishedJoiningChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, allChannels: FrozenList[str]):
        if not isinstance(allChannels, FrozenList):
            raise TypeError(f'allChannels argument is malformed: \"{allChannels}\"')

        self.__allChannels: FrozenList[str] = allChannels

    @property
    def allChannels(self) -> FrozenList[str]:
        return self.__allChannels

    @property
    def eventType(self) -> ChannelJoinEventType:
        return ChannelJoinEventType.FINISHED

    def toDictionary(self) -> dict[str, Any]:
        return {
            'allChannels': self.__allChannels,
            'eventType': self.eventType
        }
