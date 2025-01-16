from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TwitchFollowingStatus:
    followedAt: datetime
    twitchChannel: str
    twitchChannelId: str
    userId: str
    userName: str
