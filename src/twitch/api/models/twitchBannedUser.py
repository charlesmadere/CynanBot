from dataclasses import dataclass
from datetime import datetime

from ...localModels.twitchUserInterface import TwitchUserInterface


# This class intends to directly correspond to Twitch's "Get Banned Users" API:
# https://dev.twitch.tv/docs/api/reference/#get-banned-users
@dataclass(frozen = True)
class TwitchBannedUser(TwitchUserInterface):
    createdAt: datetime
    expiresAt: datetime | None
    moderatorId: str
    moderatorLogin: str
    moderatorName: str
    reason: str | None
    userId: str
    userLogin: str
    userName: str

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName
