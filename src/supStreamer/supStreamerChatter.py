from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class SupStreamerChatter:
    mostRecentSup: datetime
    twitchChannelId: str
    userId: str
