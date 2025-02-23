from dataclasses import dataclass

from ..models.ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True)
class TtsMonsterMessageChunk:
    message: str
    voice: TtsMonsterVoice
