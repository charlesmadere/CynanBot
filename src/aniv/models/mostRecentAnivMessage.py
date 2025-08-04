from dataclasses import dataclass
from datetime import datetime

from .whichAnivUser import WhichAnivUser


@dataclass(frozen = True)
class MostRecentAnivMessage:
    dateTime: datetime
    message: str | None
    whichAnivUser: WhichAnivUser
