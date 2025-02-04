from enum import Enum, auto


class TtsProvider(Enum):

    DEC_TALK = auto()
    GOOGLE = auto()
    HALF_LIFE = auto()
    MICROSOFT_SAM = auto()
    SINGING_DEC_TALK = auto()
    STREAM_ELEMENTS = auto()
    TTS_MONSTER = auto()

    @property
    def databaseName(self) -> str:
        match self:
            case TtsProvider.DEC_TALK: return 'dec_talk'
            case TtsProvider.GOOGLE: return 'google'
            case TtsProvider.HALF_LIFE: return 'half_life'
            case TtsProvider.MICROSOFT_SAM: return 'microsoft_sam'
            case TtsProvider.SINGING_DEC_TALK: return 'dec_talk'
            case TtsProvider.STREAM_ELEMENTS: return 'stream_elements'
            case TtsProvider.TTS_MONSTER: return 'tts_monster'
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{self}\"')

    @property
    def humanName(self) -> str:
        match self:
            case TtsProvider.DEC_TALK: return 'DECtalk'
            case TtsProvider.GOOGLE: return 'Google'
            case TtsProvider.HALF_LIFE: return 'Half-Life'
            case TtsProvider.MICROSOFT_SAM: return 'Microsoft Sam'
            case TtsProvider.SINGING_DEC_TALK: return 'Singing DECtalk'
            case TtsProvider.STREAM_ELEMENTS: return 'Stream Elements'
            case TtsProvider.TTS_MONSTER: return 'TTS Monster'
            case _: raise ValueError(f'Encountered unknown TtsProvider value: \"{self}\"')
