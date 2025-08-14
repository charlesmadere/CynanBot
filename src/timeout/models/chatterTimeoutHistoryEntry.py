from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class ChatterTimeoutHistoryEntry:
    dateTime: datetime
    durationSeconds: int
    chatterUserId: str
    twitchChannelId: str
