from dataclasses import dataclass
from datetime import datetime

from .voicemailData import VoicemailData


@dataclass(frozen = True, slots = True)
class PreparedVoicemailData:
    originatingUserName: str
    targetUserName: str
    voicemail: VoicemailData

    @property
    def createdDateTime(self) -> datetime:
        return self.voicemail.createdDateTime

    @property
    def message(self) -> str:
        return self.voicemail.message

    @property
    def originatingUserId(self) -> str:
        return self.voicemail.originatingUserId
