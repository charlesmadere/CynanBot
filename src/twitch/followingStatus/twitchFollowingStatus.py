from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TwitchFollowingStatus:
    followedAt: datetime
    twitchChannelId: str
    userId: str
