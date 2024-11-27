from dataclasses import dataclass

from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from src.tts.ttsProvider import TtsProvider
from ...streamElements.models.streamElementsVoice import StreamElementsVoice


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    userName: str
    voice: StreamElementsVoice | HalfLifeVoice | str | None
    ttsProvider: TtsProvider
