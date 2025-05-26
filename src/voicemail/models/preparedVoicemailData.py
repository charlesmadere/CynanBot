from dataclasses import dataclass
from datetime import datetime

from .voicemailData import VoicemailData


@dataclass(frozen = True)
class PreparedVoicemailData:
    originatingUserName: str
    preparedMessage: str
    voicemail: VoicemailData

    @property
    def createdDateTime(self) -> datetime:
        return self.voicemail.createdDateTime

    @property
    def originatingUserId(self) -> str:
        return self.voicemail.originatingUserId
