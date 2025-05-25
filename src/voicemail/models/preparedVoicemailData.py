from dataclasses import dataclass

from .voicemailData import VoicemailData


@dataclass(frozen = True)
class PreparedVoicemailData:
    originatingUserName: str
    preparedMessage: str
    voicemail: VoicemailData

    @property
    def originatingUserId(self) -> str:
        return self.voicemail.originatingUserId
