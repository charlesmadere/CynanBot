from dataclasses import dataclass
from datetime import datetime

from ...tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True)
class GlacialTtsData:
    storeDateTime: datetime
    glacialId: str
    message: str
    voice: str | None
    provider: TtsProvider
