from dataclasses import dataclass
from datetime import datetime

from .twitchBroadcasterType import TwitchBroadcasterType
from .twitchUserType import TwitchUserType
from ...localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True)
class TwitchUser(TwitchUserInterface):
    createdAt: datetime
    description: str | None
    displayName: str
    email: str | None
    profileImageUrl: str | None
    offlineImageUrl: str | None
    userId: str
    userLogin: str
    broadcasterType: TwitchBroadcasterType
    userType: TwitchUserType

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.displayName
