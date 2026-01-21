from dataclasses import dataclass
from datetime import datetime

from ...tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class GlacialTtsData:
    storeDateTime: datetime
    glacialId: str
    message: str
    voice: str | None
    provider: TtsProvider

    def requireVoice(self) -> str:
        voice = self.voice

        if voice is None:
            raise RuntimeError(f'voice value has not been set: ({self=})')

        return voice
