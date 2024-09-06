from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class ActiveChatter:
    mostRecentChat: datetime
    chatterUserId: str
    chatterUserName: str
