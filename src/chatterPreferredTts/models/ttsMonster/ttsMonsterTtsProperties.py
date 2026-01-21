from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....tts.models.ttsProvider import TtsProvider
from ....ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True, slots = True)
class TtsMonsterTtsProperties(AbsTtsProperties):
    voice: TtsMonsterVoice | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
