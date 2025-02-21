from enum import Enum, auto


class TtsMonsterVoice(Enum):

    JAZZ = auto()
    KKONA = auto()
    PIRATE = auto()
    SHADOW = auto()
    ZERO_TWO = auto()

    @property
    def humanName(self) -> str:
        match self:
            case TtsMonsterVoice.JAZZ: return 'Jazz'
            case TtsMonsterVoice.KKONA: return 'Kkona'
            case TtsMonsterVoice.PIRATE: return 'Pirate'
            case TtsMonsterVoice.SHADOW: return 'Shadow'
            case TtsMonsterVoice.ZERO_TWO: return 'Zero Two'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')
