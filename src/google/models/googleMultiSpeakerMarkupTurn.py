from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GoogleMultiSpeakerMarkupTurn:
    speaker: str
    text: str
