from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class RandoTtsTtsProperties(AbsTtsProperties):

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.RANDO_TTS
