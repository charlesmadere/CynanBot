from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class TwitchTimeoutRemodData:
    remodDateTime: datetime
    broadcasterUserId: str
    userId: str
