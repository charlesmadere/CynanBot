import locale
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TimeoutActionHistoryEntry:
    timedOutAtDateTime: datetime
    durationSeconds: int
    timedOutByUserId: str

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.durationSeconds, grouping = True)
