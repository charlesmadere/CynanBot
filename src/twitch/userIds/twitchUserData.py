from dataclasses import dataclass
from datetime import datetime

from ..localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TwitchUserData(TwitchUserInterface):
    storeDateTime: datetime
    userId: str
    userLogin: str
    userName: str

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName
