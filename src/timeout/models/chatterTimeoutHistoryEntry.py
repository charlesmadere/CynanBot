from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class ChatterTimeoutHistoryEntry:
    dateTime: datetime
    durationSeconds: int
    timedOutByUserId: str
