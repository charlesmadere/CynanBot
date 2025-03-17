from abc import ABC, abstractmethod
from typing import Any

from .channelJoinEventType import ChannelJoinEventType


class AbsChannelJoinEvent(ABC):

    @property
    @abstractmethod
    def eventType(self) -> ChannelJoinEventType:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass
