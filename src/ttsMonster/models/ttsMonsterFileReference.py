from dataclasses import dataclass
from datetime import datetime

from .ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True, slots = True)
class TtsMonsterFileReference:
    storeDateTime: datetime
    allVoices: frozenset[TtsMonsterVoice]
    filePath: str
    primaryVoice: TtsMonsterVoice
