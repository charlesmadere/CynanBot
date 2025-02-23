from enum import Enum, auto


class TtsMonsterVoice(Enum):

    BRIAN = auto()
    JAZZ = auto()
    KKONA = auto()
    PIRATE = auto()
    SHADOW = auto()
    WITCH = auto()
    ZERO_TWO = auto()

    @property
    def humanName(self) -> str:
        match self:
            case TtsMonsterVoice.BRIAN: return 'Brian'
            case TtsMonsterVoice.JAZZ: return 'Jazz'
            case TtsMonsterVoice.KKONA: return 'Kkona'
            case TtsMonsterVoice.PIRATE: return 'Pirate'
            case TtsMonsterVoice.SHADOW: return 'Shadow'
            case TtsMonsterVoice.WITCH: return 'Witch'
            case TtsMonsterVoice.ZERO_TWO: return 'Zero Two'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')

    @property
    def inMessageName(self) -> str:
        match self:
            case TtsMonsterVoice.BRIAN: return 'brian'
            case TtsMonsterVoice.JAZZ: return 'jazz'
            case TtsMonsterVoice.KKONA: return 'kkona'
            case TtsMonsterVoice.PIRATE: return 'pirate'
            case TtsMonsterVoice.SHADOW: return 'shadow'
            case TtsMonsterVoice.WITCH: return 'witch'
            case TtsMonsterVoice.ZERO_TWO: return 'zerotwo'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')
