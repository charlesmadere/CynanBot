from enum import Enum, auto


class GoogleMultiSpeakerVoicePreset(Enum):

    ENGLISH_US_R = auto()
    ENGLISH_US_S = auto()
    ENGLISH_US_T = auto()
    ENGLISH_US_U = auto()

    @property
    def fullName(self) -> str:
        match self:
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_R: return 'en-US-Studio-Multispeaker-R'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_S: return 'en-US-Studio-Multispeaker-S'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_T: return 'en-US-Studio-Multispeaker-T'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_U: return 'en-US-Studio-Multispeaker-U'
            case _: raise ValueError(f'Unknown GoogleMultiSpeakerVoicePreset value: \"{self}\"')

    @property
    def speakerCharacter(self) -> str:
        match self:
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_R: return 'R'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_S: return 'S'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_T: return 'T'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_U: return 'U'
            case _: raise ValueError(f'Unknown GoogleMultiSpeakerVoicePreset value: \"{self}\"')
