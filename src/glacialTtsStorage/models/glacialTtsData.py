from dataclasses import dataclass
from datetime import datetime

from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class GlacialTtsData:
    storeDateTime: datetime
    glacialId: str
    message: str
    provider: TtsProvider
