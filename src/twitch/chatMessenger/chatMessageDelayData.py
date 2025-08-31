from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class ChatMessageDelayData:
    now: datetime
    seconds : int
