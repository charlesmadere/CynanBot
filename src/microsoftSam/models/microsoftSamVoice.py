from enum import Enum, auto


class MicrosoftSamVoice(Enum):

    ADULT_FEMALE_1 = auto()
    ADULT_FEMALE_2 = auto()
    ADULT_MALE_1 = auto()
    ADULT_MALE_2 = auto()
    ADULT_MALE_3 = auto()
    ADULT_MALE_4 = auto()
    ADULT_MALE_5 = auto()
    ADULT_MALE_6 = auto()
    ADULT_MALE_7 = auto()
    ADULT_MALE_8 = auto()
    ADULT_FEMALE_WHISPER = auto()
    ADULT_MALE_WHISPER = auto()
    MARY = auto()
    MARY_TELEPHONE = auto()
    MARY_HALL = auto()
    MARY_SPACE = auto()
    MARY_STADIUM = auto()
    MIKE = auto()
    MIKE_TELEPHONE = auto()
    MIKE_HALL = auto()
    MIKE_SPACE = auto()
    MIKE_STADIUM = auto()
    ROBO_1 = auto()
    ROBO_2 = auto()
    ROBO_3 = auto()
    ROBO_4 = auto()
    ROBO_5 = auto()
    ROBO_6 = auto()
    SAM = auto()
    BONZI_BUDDY = auto()

    @property
    def value(self) -> str:
        match self:
            case MicrosoftSamVoice.ADULT_FEMALE_1: return 'adult_female_1'
            case MicrosoftSamVoice.ADULT_FEMALE_2: return 'adult_female_2'
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER: return 'adult_female_whisper'
            case MicrosoftSamVoice.ADULT_MALE_1: return 'adult_male_1'
            case MicrosoftSamVoice.ADULT_MALE_2: return 'adult_male_2'
            case MicrosoftSamVoice.ADULT_MALE_3: return 'adult_male_3'
            case MicrosoftSamVoice.ADULT_MALE_4: return 'adult_male_4'
            case MicrosoftSamVoice.ADULT_MALE_5: return 'adult_male_5'
            case MicrosoftSamVoice.ADULT_MALE_6: return 'adult_male_6'
            case MicrosoftSamVoice.ADULT_MALE_7: return 'adult_male_7'
            case MicrosoftSamVoice.ADULT_MALE_8: return 'adult_male_8'
            case MicrosoftSamVoice.ADULT_MALE_WHISPER: return 'adult_male_whisper'
            case MicrosoftSamVoice.BONZI_BUDDY: return 'bonzi_buddy'
            case MicrosoftSamVoice.MARY: return 'mary'
            case MicrosoftSamVoice.MARY_TELEPHONE: return 'mary_telephone'
            case MicrosoftSamVoice.MARY_HALL: return 'mary_hall'
            case MicrosoftSamVoice.MARY_SPACE: return 'mary_space'
            case MicrosoftSamVoice.MARY_STADIUM: return 'mary_stadium'
            case MicrosoftSamVoice.MIKE: return 'mike'
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 'mike_telephone'
            case MicrosoftSamVoice.MIKE_HALL: return 'mike_hall'
            case MicrosoftSamVoice.MIKE_SPACE: return 'mike_space'
            case MicrosoftSamVoice.MIKE_STADIUM: return 'mike_stadium'
            case MicrosoftSamVoice.ROBO_1: return 'robo_1'
            case MicrosoftSamVoice.ROBO_2: return 'robo_2'
            case MicrosoftSamVoice.ROBO_3: return 'robo_3'
            case MicrosoftSamVoice.ROBO_4: return 'robo_4'
            case MicrosoftSamVoice.ROBO_5: return 'robo_5'
            case MicrosoftSamVoice.ROBO_6: return 'robo_6'
            case MicrosoftSamVoice.SAM: return 'sam'
            case _: raise RuntimeError(f'unknown Microsoft Sam voice: \"{self}\"')
