from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class MostRecentChat():
    mostRecentChat: datetime
    twitchChannelId: str
    userId: str
