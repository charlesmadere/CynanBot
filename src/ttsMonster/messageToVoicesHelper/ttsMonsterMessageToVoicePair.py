from dataclasses import dataclass

from ..models.ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True)
class TtsMonsterMessageToVoicePair:
    message: str
    voice: TtsMonsterVoice
