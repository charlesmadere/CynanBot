from dataclasses import dataclass
from typing import Any


@dataclass(frozen = True)
class BasicTimeoutTarget:
    targetUserId: str
    targetUserName: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BasicTimeoutTarget):
            return False

        return self.targetUserId == other.targetUserId

    def __hash__(self) -> int:
        return hash(self.targetUserId)
