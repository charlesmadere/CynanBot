from dataclasses import dataclass

from ...voicemail.models.addVoicemailResult import AddVoicemailResult


@dataclass(frozen = True)
class CassetteTapeUseCaseResult:
    addVoicemailResult: AddVoicemailResult
    targetUserId: str
    targetUserName: str
