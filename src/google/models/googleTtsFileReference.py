from dataclasses import dataclass
from datetime import datetime

from .absGoogleVoicePreset import AbsGoogleVoicePreset


@dataclass(frozen = True, slots = True)
class GoogleTtsFileReference:
    voicePreset: AbsGoogleVoicePreset
    storeDateTime: datetime
    filePath: str
