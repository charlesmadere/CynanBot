from dataclasses import dataclass

from .googleVoiceGender import GoogleVoiceGender


@dataclass(frozen = True, slots = True)
class GoogleVoiceSelectionParams:
    gender: GoogleVoiceGender | None
    languageCode: str
    name: str | None
