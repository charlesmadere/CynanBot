from enum import Enum, auto

from .absGoogleVoicePreset import AbsGoogleVoicePreset


class GoogleMultiSpeakerVoicePreset(AbsGoogleVoicePreset, Enum):

    ENGLISH_US_STUDIO_MULTI_SPEAKER = auto()

    @property
    def fullName(self) -> str:
        match self:
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER: return 'en-US-Studio-MultiSpeaker'
            case _: raise ValueError(f'Unknown GoogleMultiSpeakerVoicePreset value: \"{self}\"')

    @property
    def speakerCharacters(self) -> frozenset[str]:
        speakerCharacters: set[str] = set()

        match self:
            case GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER:
                speakerCharacters = { 'R', 'S', 'T', 'U' }

            case _:
                raise ValueError(f'Unknown GoogleMultiSpeakerVoicePreset value: \"{self}\"')

        return frozenset(speakerCharacters)
