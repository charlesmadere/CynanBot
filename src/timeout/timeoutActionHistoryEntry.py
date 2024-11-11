import locale
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TimeoutActionHistoryEntry:
    timedOutAtDateTime: datetime
    bitAmount: int
    durationSeconds: int
    timedOutByUserId: str

    @property
    def bitAmountStr(self) -> str:
        return locale.format_string("%d", self.bitAmount, grouping = True)

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.durationSeconds, grouping = True)
