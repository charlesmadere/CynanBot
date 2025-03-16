from enum import Enum, auto


class TtsMonsterVoice(Enum):

    ADAM = auto()
    ASMR = auto()
    BRIAN = auto()
    HIKARI = auto()
    JAZZ = auto()
    KKONA = auto()
    NARRATOR = auto()
    PIRATE = auto()
    SHADOW = auto()
    WITCH = auto()
    ZERO_TWO = auto()

    @property
    def humanName(self) -> str:
        match self:
            case TtsMonsterVoice.ADAM: return 'Adam'
            case TtsMonsterVoice.ASMR: return 'ASMR'
            case TtsMonsterVoice.BRIAN: return 'Brian'
            case TtsMonsterVoice.HIKARI: return 'Hikari'
            case TtsMonsterVoice.JAZZ: return 'Jazz'
            case TtsMonsterVoice.KKONA: return 'Kkona'
            case TtsMonsterVoice.NARRATOR: return 'Narrator'
            case TtsMonsterVoice.PIRATE: return 'Pirate'
            case TtsMonsterVoice.SHADOW: return 'Shadow'
            case TtsMonsterVoice.WITCH: return 'Witch'
            case TtsMonsterVoice.ZERO_TWO: return 'Zero Two'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')

    @property
    def inMessageName(self) -> str:
        match self:
            case TtsMonsterVoice.ADAM: return 'adam'
            case TtsMonsterVoice.ASMR: return 'asmr'
            case TtsMonsterVoice.BRIAN: return 'brian'
            case TtsMonsterVoice.HIKARI: return 'hikari'
            case TtsMonsterVoice.JAZZ: return 'jazz'
            case TtsMonsterVoice.KKONA: return 'kkona'
            case TtsMonsterVoice.NARRATOR: return 'narrator'
            case TtsMonsterVoice.PIRATE: return 'pirate'
            case TtsMonsterVoice.SHADOW: return 'shadow'
            case TtsMonsterVoice.WITCH: return 'witch'
            case TtsMonsterVoice.ZERO_TWO: return 'zerotwo'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')
