from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True)
class MicrosoftTtsTtsProperties(AbsTtsProperties):
    voice: MicrosoftTtsVoice | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT
