from dataclasses import dataclass


@dataclass(frozen = True)
class MicrosoftSamVoiceData:
    voice: str
    pitch: str
    speed: str
