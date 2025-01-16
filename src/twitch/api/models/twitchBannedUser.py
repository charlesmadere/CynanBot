from dataclasses import dataclass
from datetime import datetime


# This class intends to directly correspond to Twitch's "Get Banned Users" API:
# https://dev.twitch.tv/docs/api/reference/#get-banned-users
@dataclass(frozen = True)
class TwitchBannedUser:
    createdAt: datetime
    expiresAt: datetime | None
    moderatorId: str
    moderatorLogin: str
    moderatorName: str
    reason: str | None
    userId: str
    userLogin: str
    userName: str
