from dataclasses import dataclass
from typing import Any

from ..localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TwitchWebsocketUser(TwitchUserInterface):
    userId: str
    userLogin: str
    userName: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TwitchUserInterface):
            return False

        return self.userId == other.getUserId()

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName

    def __hash__(self) -> int:
        return hash(self.userId)
