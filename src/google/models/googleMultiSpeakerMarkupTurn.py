from dataclasses import dataclass

from .googleMultiSpeakerVoicePreset import GoogleMultiSpeakerVoicePreset


@dataclass(frozen = True)
class GoogleMultiSpeakerMarkupTurn:
    speaker: GoogleMultiSpeakerVoicePreset
    text: str
