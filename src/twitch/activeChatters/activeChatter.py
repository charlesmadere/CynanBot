from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen = True)
class ActiveChatter:
    mostRecentMessage: datetime
    chatterUserId: str
    chatterUserName: str
