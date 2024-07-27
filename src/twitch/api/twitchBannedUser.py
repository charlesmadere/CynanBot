from dataclasses import dataclass
from datetime import datetime


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
