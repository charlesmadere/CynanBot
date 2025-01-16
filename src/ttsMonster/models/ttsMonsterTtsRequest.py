from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterTtsRequest:
    returnUsage: bool
    message: str
    voiceId: str
