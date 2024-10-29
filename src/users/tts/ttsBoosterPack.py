from dataclasses import dataclass

from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class TtsBoosterPack:
    cheerAmount: int
    ttsProvider: TtsProvider