from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class ShotgunTtsTtsProperties(AbsTtsProperties):

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.SHOTGUN_TTS
