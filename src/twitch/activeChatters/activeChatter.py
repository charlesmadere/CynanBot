from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen = True)
class ActiveChatter:
    mostRecentChat: datetime
    chatterUserId: str
    chatterUserName: str
