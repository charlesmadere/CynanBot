from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TwitchFollower():
    followedAt: datetime
    userId: str
    userLogin: str
    userName: str
