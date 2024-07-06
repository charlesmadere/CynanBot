import locale
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AbsCheerAction):
            return False

        return self.bits == other.bits and self.twitchChannelId == other.twitchChannelId

    def __hash__(self) -> int:
        return hash((self.bits, self.twitchChannelId))
