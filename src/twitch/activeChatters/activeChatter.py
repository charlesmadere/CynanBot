from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen = True, slots = True)
class ActiveChatter:
    mostRecentChat: datetime
    chatterUserId: str
    chatterUserName: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ActiveChatter):
            return False

        return self.chatterUserId == other.chatterUserId

    def __hash__(self) -> int:
        return hash(self.chatterUserId)
