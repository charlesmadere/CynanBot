import locale
from abc import ABC, abstractmethod
from typing import Any

from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType


class AbsCheerAction(ABC):

    @property
    def bitsString(self) -> str:
        return locale.format_string("%d", self.getBits(), grouping = True)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AbsCheerAction):
            return False

        return self.getBits() == other.getBits() and self.getTwitchChannelId() == other.getTwitchChannelId()

    @property
    @abstractmethod
    def actionType(self) -> CheerActionType:
        pass

    @abstractmethod
    def getBits(self) -> int:
        pass

    @abstractmethod
    def getStreamStatusRequirement(self) -> CheerActionStreamStatusRequirement:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass

    def __hash__(self) -> int:
        return hash((self.getBits(), self.getTwitchChannelId()))

    @abstractmethod
    def isEnabled(self) -> bool:
        pass

    @abstractmethod
    def printOut(self) -> str:
        pass
