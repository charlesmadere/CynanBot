from dataclasses import dataclass
from datetime import datetime


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
@dataclass(frozen = True)
class TwitchBanResponse:
    createdAt: datetime
    endTime: datetime | None
    broadcasterUserId: str
    moderatorUserId: str
    userId: str
