import locale
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class WatchStreakStats:
    mostRecentUpdate: datetime
    bestStreak: int
    currentStreak: int
    chatterUserId: str
    twitchChannelId: str

    @property
    def bestStreakStr(self) -> str:
        return locale.format_string("%d", self.bestStreak, grouping = True)

    @property
    def currentStreakStr(self) -> str:
        return locale.format_string("%d", self.currentStreak, grouping = True)
