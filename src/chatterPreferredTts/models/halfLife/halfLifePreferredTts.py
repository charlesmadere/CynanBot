from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....halfLife.models.halfLifeVoice import HalfLifeVoice
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True)
class HalfLifeTtsProperties(AbsTtsProperties):
    voice: HalfLifeVoice | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE
