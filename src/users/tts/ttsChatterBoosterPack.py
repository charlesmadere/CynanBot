from dataclasses import dataclass

from ...streamElements.models.streamElementsVoice import StreamElementsVoice


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    userName: str
    voice: StreamElementsVoice
