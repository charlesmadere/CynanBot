from enum import Enum, auto


class TtsProvider(Enum):

    COMMODORE_SAM = auto()
    DEC_TALK = auto()
    GOOGLE = auto()
    HALF_LIFE = auto()
    MICROSOFT = auto()
    MICROSOFT_SAM = auto()
    RANDO_TTS = auto()
    SHOTGUN_TTS = auto()
    STREAM_ELEMENTS = auto()
    TTS_MONSTER = auto()
    UNRESTRICTED_DEC_TALK = auto()

    @property
    def humanName(self) -> str:
        match self:
            case TtsProvider.COMMODORE_SAM: return 'Commodore SAM'
            case TtsProvider.DEC_TALK: return 'DECtalk'
            case TtsProvider.GOOGLE: return 'Google'
            case TtsProvider.HALF_LIFE: return 'Half-Life'
            case TtsProvider.MICROSOFT: return 'Microsoft'
            case TtsProvider.MICROSOFT_SAM: return 'Microsoft Sam'
            case TtsProvider.RANDO_TTS: return 'Rando TTS'
            case TtsProvider.SHOTGUN_TTS: return 'Shotgun TTS'
            case TtsProvider.STREAM_ELEMENTS: return 'Stream Elements'
            case TtsProvider.TTS_MONSTER: return 'TTS Monster'
            case TtsProvider.UNRESTRICTED_DEC_TALK: return 'Unrestricted DECtalk'
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{self}\"')
