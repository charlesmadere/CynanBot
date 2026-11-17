from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class ActiveChatter(TwitchUserInterface):
    mostRecentChat: datetime
    chatterUserId: str
    chatterUserLogin: str
    chatterUserName: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TwitchUserInterface):
            return False

        return self.chatterUserId == other.getUserId()

    def getUserId(self) -> str:
        return self.chatterUserId

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName

    def __hash__(self) -> int:
        return hash(self.chatterUserId)
