from dataclasses import dataclass
from typing import Any


@dataclass(frozen = True)
class TtsMonsterVoice:
    language: str | None
    metadata: str | None
    name: str
    sample: str | None
    voiceId: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TtsMonsterVoice):
            return False

        return self.voiceId == other.voiceId

    def __hash__(self) -> int:
        return hash(self.voiceId)
