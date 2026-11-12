from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class WatchStreakRewardHistoryData:
    mostRecentReward: datetime
    watchStreak: int
