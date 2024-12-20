from dataclasses import dataclass

from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    userName: str
    voice: MicrosoftSamVoice | StreamElementsVoice | HalfLifeVoice | str | None
    ttsProvider: TtsProvider
