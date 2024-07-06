import locale
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType


@dataclass(frozen = True)
class AbsCheerAction(ABC):
    isEnabled: bool
    streamStatusRequirement: CheerActionStreamStatusRequirement
    bits: int
    twitchChannel: str
    twitchChannelId: str

    @property
    @abstractmethod
    def actionType(self) -> CheerActionType:
        pass

    @property
    def bitsString(self) -> str:
        return locale.format_string("%d", self.bits, grouping = True)
