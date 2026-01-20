from dataclasses import dataclass
from datetime import datetime


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
@dataclass(frozen = True, slots = True)
class TwitchBanResponseEntry:
    createdAt: datetime
    endTime: datetime | None
    broadcasterId: str
    moderatorId: str
    userId: str
