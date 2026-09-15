from dataclasses import dataclass
from datetime import datetime

from .useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class CrowdMicrophoneStatus:
    endTime: datetime
    totalDurationSeconds: int
    twitchChannelId: str
    originatingAction: UseChatterItemAction
