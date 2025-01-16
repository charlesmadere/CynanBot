from dataclasses import dataclass
from typing import Any

from .ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


@dataclass(frozen = True)
class TtsMonsterVoice:
    language: str | None
    metadata: str | None
    name: str
    sample: str | None
    voiceId: str
    websiteVoice: TtsMonsterWebsiteVoice | None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TtsMonsterVoice):
            return False

        return self.voiceId == other.voiceId

    def __hash__(self) -> int:
        return hash(self.voiceId)

    def requireWebsiteVoice(self) -> TtsMonsterWebsiteVoice:
        if self.websiteVoice is None:
            raise ValueError(f'No `websiteVoice` value was set! ({self=})')

        return self.websiteVoice
