from dataclasses import dataclass
from datetime import datetime

from .googleVoicePreset import GoogleVoicePreset


@dataclass(frozen = True, slots = True)
class GoogleTtsFileReference:
    storeDateTime: datetime
    voicePreset: GoogleVoicePreset
    filePath: str
