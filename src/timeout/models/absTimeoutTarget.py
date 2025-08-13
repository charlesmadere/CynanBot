from abc import ABC, abstractmethod
from typing import Any


class AbsTimeoutTarget(ABC):

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AbsTimeoutTarget):
            return False

        return self.getTargetUserId() == other.getTargetUserId()

    @abstractmethod
    def getTargetUserId(self) -> str:
        pass

    @abstractmethod
    def getTargetUserName(self) -> str:
        pass

    def __hash__(self) -> int:
        return hash(self.getTargetUserId())
