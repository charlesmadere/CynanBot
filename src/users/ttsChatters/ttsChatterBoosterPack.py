from dataclasses import dataclass

from src.tts.ttsProvider import TtsProvider

from ...streamElements.models.streamElementsVoice import StreamElementsVoice


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    userName: str
    voice: StreamElementsVoice | str | None
    ttsProvider: TtsProvider
