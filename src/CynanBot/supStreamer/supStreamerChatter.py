from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen = True)
class SupStreamerChatter():
    mostRecentSup: datetime | None
    twitchChannelId: str
    userId: str

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, SupStreamerChatter):
            return self.userId == value.userId
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.userId)
