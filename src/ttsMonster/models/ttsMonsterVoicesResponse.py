from dataclasses import dataclass

from frozenlist import FrozenList

from .ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True)
class TtsMonsterVoicesResponse:
    customVoices: FrozenList[TtsMonsterVoice] | None
    voices: FrozenList[TtsMonsterVoice] | None
