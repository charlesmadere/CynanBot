from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....decTalk.models.decTalkVoice import DecTalkVoice
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True)
class DecTalkTtsProperties(AbsTtsProperties):
    voice: DecTalkVoice | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
