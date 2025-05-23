from dataclasses import dataclass


@dataclass(frozen = True)
class VoicemailData:
    message: str
    originatingUserId: str
    targetUserId: str
    twitchChannelId: str
    voicemailId: str
