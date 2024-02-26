from enum import Enum, auto


class GoogleVoiceGender(Enum):

    FEMALE = auto()
    MALE = auto()
    UNSPECIFIED = auto()

    def toStr(self) -> str:
        if self is GoogleVoiceGender.FEMALE:
            return 'FEMALE'
        elif self is GoogleVoiceGender.MALE:
            return 'MALE'
        elif self is GoogleVoiceGender.UNSPECIFIED:
            return 'SSML_VOICE_GENDER_UNSPECIFIED'
        else:
            raise RuntimeError(f'unknown GoogleVoiceGender: \"{self}\"')
