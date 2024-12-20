from enum import Enum, auto

class MicrosoftSamVoice(Enum):

    ADULT_MALE_2 = auto()
    SAM = auto()
    ROBO_4 = auto()

    @property
    def value(self) -> str:
        match self:
            case MicrosoftSamVoice.ADULT_MALE_2: return 'adult_male_2'
            case MicrosoftSamVoice.SAM: return 'sam'
            case MicrosoftSamVoice.ROBO_4: return 'robo_4'
            case _: raise RuntimeError(f'unknown Microsoft Sam voice: \"{self}\"')