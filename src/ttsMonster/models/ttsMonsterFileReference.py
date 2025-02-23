from dataclasses import dataclass
from datetime import datetime

from .ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True)
class TtsMonsterFileReference:
    storeDateTime: datetime
    messageVoices: frozenset[TtsMonsterVoice]
    filePath: str
