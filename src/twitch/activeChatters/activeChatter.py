from dataclasses import dataclass
from datetime import datetime

from ..localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class ActiveChatter(TwitchUserInterface):
    mostRecentChat: datetime
    chatterUserId: str
    chatterUserLogin: str
    chatterUserName: str

    def getUserId(self) -> str:
        return self.chatterUserId

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName
