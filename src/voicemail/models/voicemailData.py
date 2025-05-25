from dataclasses import dataclass
from datetime import datetime

from ...tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True)
class VoicemailData:
    createdDateTime: datetime
    message: str
    originatingUserId: str
    targetUserId: str
    twitchChannelId: str
    voicemailId: str
    ttsProvider: TtsProvider | None
