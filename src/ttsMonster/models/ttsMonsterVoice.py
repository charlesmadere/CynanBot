from enum import Enum, auto


class TtsMonsterVoice(Enum):

    ADAM = auto()
    ANNOUNCER = auto()
    ASMR = auto()
    BRIAN = auto()
    GLADOS = auto()
    HIKARI = auto()
    JAZZ = auto()
    JOHNNY = auto()
    KKONA = auto()
    NARRATOR = auto()
    PIRATE = auto()
    SHADOW = auto()
    SONIC = auto()
    SPONGEBOB = auto()
    VOMIT = auto()
    WEEB = auto()
    WITCH = auto()
    ZERO_TWO = auto()
    ZOOMER = auto()

    @property
    def humanName(self) -> str:
        match self:
            case TtsMonsterVoice.ADAM: return 'Adam'
            case TtsMonsterVoice.ANNOUNCER: return 'Announcer'
            case TtsMonsterVoice.ASMR: return 'ASMR'
            case TtsMonsterVoice.BRIAN: return 'Brian'
            case TtsMonsterVoice.GLADOS: return 'Glados'
            case TtsMonsterVoice.HIKARI: return 'Hikari'
            case TtsMonsterVoice.JAZZ: return 'Jazz'
            case TtsMonsterVoice.JOHNNY: return 'Johnny'
            case TtsMonsterVoice.KKONA: return 'Kkona'
            case TtsMonsterVoice.NARRATOR: return 'Narrator'
            case TtsMonsterVoice.PIRATE: return 'Pirate'
            case TtsMonsterVoice.SHADOW: return 'Shadow'
            case TtsMonsterVoice.SONIC: return 'Sonic'
            case TtsMonsterVoice.SPONGEBOB: return 'Spongebob'
            case TtsMonsterVoice.VOMIT: return 'Vomit'
            case TtsMonsterVoice.WEEB: return 'Weeb'
            case TtsMonsterVoice.WITCH: return 'Witch'
            case TtsMonsterVoice.ZERO_TWO: return 'Zero Two'
            case TtsMonsterVoice.ZOOMER: return 'Zoomer'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')

    @property
    def inMessageName(self) -> str:
        match self:
            case TtsMonsterVoice.ADAM: return 'adam'
            case TtsMonsterVoice.ANNOUNCER: return 'announcer'
            case TtsMonsterVoice.ASMR: return 'asmr'
            case TtsMonsterVoice.BRIAN: return 'brian'
            case TtsMonsterVoice.GLADOS: return 'glados'
            case TtsMonsterVoice.HIKARI: return 'hikari'
            case TtsMonsterVoice.JAZZ: return 'jazz'
            case TtsMonsterVoice.JOHNNY: return 'johnny'
            case TtsMonsterVoice.KKONA: return 'kkona'
            case TtsMonsterVoice.NARRATOR: return 'narrator'
            case TtsMonsterVoice.PIRATE: return 'pirate'
            case TtsMonsterVoice.SHADOW: return 'shadow'
            case TtsMonsterVoice.SONIC: return 'sonic'
            case TtsMonsterVoice.SPONGEBOB: return 'spongebob'
            case TtsMonsterVoice.VOMIT: return 'vomit'
            case TtsMonsterVoice.WEEB: return 'weeb'
            case TtsMonsterVoice.WITCH: return 'witch'
            case TtsMonsterVoice.ZERO_TWO: return 'zerotwo'
            case TtsMonsterVoice.ZOOMER: return 'zoomer'
            case _: raise ValueError(f'Unknown TtsMonsterVoice value: \"{self}\"')
