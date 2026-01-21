from dataclasses import dataclass
from typing import Any


@dataclass(frozen = True, slots = True)
class TimeoutTarget:
    userId: str
    userName: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimeoutTarget):
            return False

        return self.userId == other.userId

    def __hash__(self) -> int:
        return hash(self.userId)
