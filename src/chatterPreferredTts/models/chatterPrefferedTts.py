from dataclasses import dataclass

from .absTtsProperties import AbsTtsProperties
from ...tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class ChatterPreferredTts:
    properties: AbsTtsProperties
    chatterUserId: str
    twitchChannelId: str

    @property
    def provider(self) -> TtsProvider:
        return self.properties.provider
