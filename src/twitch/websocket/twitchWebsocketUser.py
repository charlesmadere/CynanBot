from dataclasses import dataclass
from typing import Any


@dataclass(frozen = True, slots = True)
class TwitchWebsocketUser:
    userId: str
    userName: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TwitchWebsocketUser):
            return False

        return self.userId == other.userId

    def __hash__(self) -> int:
        return hash(self.userId)

    def __repr__(self) -> str:
        return self.userName
