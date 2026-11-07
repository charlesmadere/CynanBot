from dataclasses import dataclass
from datetime import datetime

import locale


@dataclass(frozen = True, slots = True)
class WatchStreakStats:
    mostRecentUpdate: datetime
    bestEverStreak: int
    currentStreak: int
    chatterUserId: str
    twitchChannelId: str

    @property
    def bestEverStreakStr(self) -> str:
        return locale.format_string("%d", self.bestEverStreak, grouping = True)

    @property
    def currentStreakStr(self) -> str:
        return locale.format_string("%d", self.currentStreak, grouping = True)
