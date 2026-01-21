from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class MicrosoftSamTtsProperties(AbsTtsProperties):
    voice: MicrosoftSamVoice | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
