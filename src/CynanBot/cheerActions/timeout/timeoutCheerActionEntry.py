from dataclasses import dataclass
from datetime import datetime
import locale


@dataclass(frozen = True)
class TimeoutCheerActionEntry():
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
