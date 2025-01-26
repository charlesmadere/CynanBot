from dataclasses import dataclass


from ..accessLevel.accessLevel import AccessLevel
from ...halfLife.models.halfLifeVoice import HalfLifeVoice
from ...microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ...streamElements.models.streamElementsVoice import StreamElementsVoice
from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class TtsChatterBoosterPack:
    accessLevel: AccessLevel
    ttsProvider: TtsProvider
    userName: str
    voice: MicrosoftSamVoice | StreamElementsVoice | HalfLifeVoice | str | None
