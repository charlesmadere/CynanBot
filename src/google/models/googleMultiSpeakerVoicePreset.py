from enum import Enum, auto


class GoogleMultiSpeakerVoicePreset(Enum):

    ENGLISH_US_STUDIO_MULTI_SPEAKER_R = auto()
    ENGLISH_US_STUDIO_MULTI_SPEAKER_S = auto()
    ENGLISH_US_STUDIO_MULTI_SPEAKER_T = auto()
    ENGLISH_US_STUDIO_MULTI_SPEAKER_U = auto()

    @property
    def fullName(self) -> str:
        match self:
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_R: return 'en-US-Studio-Multispeaker-R'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_S: return 'en-US-Studio-Multispeaker-S'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_T: return 'en-US-Studio-Multispeaker-T'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_U: return 'en-US-Studio-Multispeaker-U'
            case _: raise ValueError(f'Unknown GoogleMultiSpeakerVoicePreset value: \"{self}\"')

    @property
    def languageCode(self) -> str:
        return "-".join(self.fullName.split("-")[:2])

    @property
    def speakerCharacter(self) -> str:
        match self:
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_R: return 'R'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_S: return 'S'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_T: return 'T'
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER_U: return 'U'
            case _: raise ValueError(f'Unknown GoogleMultiSpeakerVoicePreset value: \"{self}\"')
