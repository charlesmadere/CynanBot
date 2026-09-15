from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class CrowdMicrophoneStatus:
    endTime: datetime
    totalDurationSeconds: int
    twitchChannelId: str
