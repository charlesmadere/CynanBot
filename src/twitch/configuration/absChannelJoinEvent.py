from abc import ABC, abstractmethod

from .channelJoinEventType import ChannelJoinEventType


class AbsChannelJoinEvent(ABC):

    @abstractmethod
    def getEventType(self) -> ChannelJoinEventType:
        pass
