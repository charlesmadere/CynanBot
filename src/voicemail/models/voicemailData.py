from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class VoicemailData:
    createdDateTime: datetime
    message: str
    originatingUserId: str
    targetUserId: str
    twitchChannelId: str
    voicemailId: str
