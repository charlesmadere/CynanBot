from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterVoice:
    language: str | None
    metadata: str | None
    name: str
    sample: str | None
    voiceId: str
