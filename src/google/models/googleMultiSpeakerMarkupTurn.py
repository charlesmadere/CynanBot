from dataclasses import dataclass


@dataclass(frozen = True)
class GoogleMultiSpeakerMarkupTurn:
    speaker: str
    text: str
