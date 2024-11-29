from dataclasses import dataclass

from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    userName: str
    voice: StreamElementsVoice | HalfLifeVoice | str | None
    ttsProvider: TtsProvider
