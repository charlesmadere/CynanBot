from abc import ABC, abstractmethod
from dataclasses import dataclass

from .chatEventType import ChatEventType
from ..misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class AbsChatMessage(ABC):
    dateTime: SimpleDateTime
    twitchChannel: str
    twitchChannelId: str

    @property
    @abstractmethod
    def chatEventType(self) -> ChatEventType:
        pass
