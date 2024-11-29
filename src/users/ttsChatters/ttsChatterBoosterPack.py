from dataclasses import dataclass

from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    userName: str
    voice: StreamElementsVoice | str | None
    ttsProvider: TtsProvider
