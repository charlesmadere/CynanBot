from dataclasses import dataclass
from typing import Any


@dataclass(frozen = True)
class GrenadeTargetData:
    targetUserId: str
    targetUserName: str

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, GrenadeTargetData):
            return self.targetUserId == other.targetUserId
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.targetUserId)
