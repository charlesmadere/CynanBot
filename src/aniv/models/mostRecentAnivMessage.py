from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class MostRecentAnivMessage:
    dateTime: datetime
    message: str | None
