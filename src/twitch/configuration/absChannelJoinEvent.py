from abc import ABC, abstractmethod

from .channelJoinEventType import ChannelJoinEventType


class AbsChannelJoinEvent(ABC):

    @property
    @abstractmethod
    def eventType(self) -> ChannelJoinEventType:
        pass
