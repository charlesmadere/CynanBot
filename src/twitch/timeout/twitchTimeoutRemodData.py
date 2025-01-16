from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TwitchTimeoutRemodData:
    remodDateTime: datetime
    broadcasterUserId: str
    broadcasterUserName: str
    userId: str
