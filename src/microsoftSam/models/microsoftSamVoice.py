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
    BONZI_BUDDY = auto()
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

    @property
    def apiValue(self) -> str:
        match self:
            case MicrosoftSamVoice.ADULT_FEMALE_1: return 'Adult Female #1, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_FEMALE_2: return 'Adult Female #2, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER: return 'Female Whisper'
            case MicrosoftSamVoice.ADULT_MALE_1: return 'Adult Male #1, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_2: return 'Adult Male #2, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_3: return 'Adult Male #3, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_4: return 'Adult Male #4, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_5: return 'Adult Male #5, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_6: return 'Adult Male #6, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_7: return 'Adult Male #7, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_8: return 'Adult Male #8, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_WHISPER: return 'Male Whisper'
            case MicrosoftSamVoice.BONZI_BUDDY: return 'Adult Male #2, American English (TruVoice)'
            case MicrosoftSamVoice.MARY: return 'Mary'
            case MicrosoftSamVoice.MARY_HALL: return 'Mary in Hall'
            case MicrosoftSamVoice.MARY_SPACE: return 'Mary in Space'
            case MicrosoftSamVoice.MARY_STADIUM: return 'Mary in Stadium'
            case MicrosoftSamVoice.MARY_TELEPHONE: return 'Mary (for Telephone)'
            case MicrosoftSamVoice.MIKE: return 'Mike'
            case MicrosoftSamVoice.MIKE_HALL: return 'Mike in Hall'
            case MicrosoftSamVoice.MIKE_SPACE: return 'Mike in Space'
            case MicrosoftSamVoice.MIKE_STADIUM: return 'Mike in Stadium'
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 'Mike (for Telephone)'
            case MicrosoftSamVoice.ROBO_1: return 'RoboSoft One'
            case MicrosoftSamVoice.ROBO_2: return 'RoboSoft Two'
            case MicrosoftSamVoice.ROBO_3: return 'RoboSoft Three'
            case MicrosoftSamVoice.ROBO_4: return 'RoboSoft Four'
            case MicrosoftSamVoice.ROBO_5: return 'RoboSoft Five'
            case MicrosoftSamVoice.ROBO_6: return 'RoboSoft Six'
            case MicrosoftSamVoice.SAM: return 'Sam'
            case _: raise RuntimeError(f'Unknown MicrosoftSamVoice value: \"{self}\"')

    @property
    def humanName(self) -> str:
        match self:
            case MicrosoftSamVoice.ADULT_FEMALE_1: return 'Adult Female #1, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_FEMALE_2: return 'Adult Female #2, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER: return 'Female Whisper'
            case MicrosoftSamVoice.ADULT_MALE_1: return 'Adult Male #1, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_2: return 'Adult Male #2, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_3: return 'Adult Male #3, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_4: return 'Adult Male #4, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_5: return 'Adult Male #5, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_6: return 'Adult Male #6, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_7: return 'Adult Male #7, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_8: return 'Adult Male #8, American English (TruVoice)'
            case MicrosoftSamVoice.ADULT_MALE_WHISPER: return 'Male Whisper'
            case MicrosoftSamVoice.BONZI_BUDDY: return 'Bonzi Buddy'
            case MicrosoftSamVoice.MARY: return 'Mary'
            case MicrosoftSamVoice.MARY_HALL: return 'Mary in Hall'
            case MicrosoftSamVoice.MARY_SPACE: return 'Mary in Space'
            case MicrosoftSamVoice.MARY_STADIUM: return 'Mary in Stadium'
            case MicrosoftSamVoice.MARY_TELEPHONE: return 'Mary (for Telephone)'
            case MicrosoftSamVoice.MIKE: return 'Mike'
            case MicrosoftSamVoice.MIKE_HALL: return 'Mike in Hall'
            case MicrosoftSamVoice.MIKE_SPACE: return 'Mike in Space'
            case MicrosoftSamVoice.MIKE_STADIUM: return 'Mike in Stadium'
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 'Mike (for Telephone)'
            case MicrosoftSamVoice.ROBO_1: return 'RoboSoft One'
            case MicrosoftSamVoice.ROBO_2: return 'RoboSoft Two'
            case MicrosoftSamVoice.ROBO_3: return 'RoboSoft Three'
            case MicrosoftSamVoice.ROBO_4: return 'RoboSoft Four'
            case MicrosoftSamVoice.ROBO_5: return 'RoboSoft Five'
            case MicrosoftSamVoice.ROBO_6: return 'RoboSoft Six'
            case MicrosoftSamVoice.SAM: return 'Sam'
            case _: raise RuntimeError(f'Unknown MicrosoftSamVoice value: \"{self}\"')

    @property
    def jsonValue(self) -> str:
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
            case MicrosoftSamVoice.MARY_HALL: return 'mary_hall'
            case MicrosoftSamVoice.MARY_SPACE: return 'mary_space'
            case MicrosoftSamVoice.MARY_STADIUM: return 'mary_stadium'
            case MicrosoftSamVoice.MARY_TELEPHONE: return 'mary_telephone'
            case MicrosoftSamVoice.MIKE: return 'mike'
            case MicrosoftSamVoice.MIKE_HALL: return 'mike_hall'
            case MicrosoftSamVoice.MIKE_SPACE: return 'mike_space'
            case MicrosoftSamVoice.MIKE_STADIUM: return 'mike_stadium'
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 'mike_telephone'
            case MicrosoftSamVoice.ROBO_1: return 'robo_1'
            case MicrosoftSamVoice.ROBO_2: return 'robo_2'
            case MicrosoftSamVoice.ROBO_3: return 'robo_3'
            case MicrosoftSamVoice.ROBO_4: return 'robo_4'
            case MicrosoftSamVoice.ROBO_5: return 'robo_5'
            case MicrosoftSamVoice.ROBO_6: return 'robo_6'
            case MicrosoftSamVoice.SAM: return 'sam'
            case _: raise RuntimeError(f'Unknown MicrosoftSamVoice value: \"{self}\"')

    @property
    def pitch(self) -> int:
        match self:
            case MicrosoftSamVoice.ADULT_FEMALE_1: return 208
            case MicrosoftSamVoice.ADULT_FEMALE_2: return 152
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER: return 169
            case MicrosoftSamVoice.ADULT_MALE_1: return 85
            case MicrosoftSamVoice.ADULT_MALE_2: return 50
            case MicrosoftSamVoice.ADULT_MALE_3: return 125
            case MicrosoftSamVoice.ADULT_MALE_4: return 73
            case MicrosoftSamVoice.ADULT_MALE_5: return 129
            case MicrosoftSamVoice.ADULT_MALE_6: return 89
            case MicrosoftSamVoice.ADULT_MALE_7: return 117
            case MicrosoftSamVoice.ADULT_MALE_8: return 203
            case MicrosoftSamVoice.ADULT_MALE_WHISPER: return 113
            case MicrosoftSamVoice.BONZI_BUDDY: return 140
            case MicrosoftSamVoice.MARY: return 169
            case MicrosoftSamVoice.MARY_HALL: return 169
            case MicrosoftSamVoice.MARY_SPACE: return 169
            case MicrosoftSamVoice.MARY_STADIUM: return 169
            case MicrosoftSamVoice.MARY_TELEPHONE: return 169
            case MicrosoftSamVoice.MIKE: return 113
            case MicrosoftSamVoice.MIKE_HALL: return 113
            case MicrosoftSamVoice.MIKE_SPACE: return 113
            case MicrosoftSamVoice.MIKE_STADIUM: return 113
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 113
            case MicrosoftSamVoice.ROBO_1: return 75
            case MicrosoftSamVoice.ROBO_2: return 120
            case MicrosoftSamVoice.ROBO_3: return 113
            case MicrosoftSamVoice.ROBO_4: return 169
            case MicrosoftSamVoice.ROBO_5: return 120
            case MicrosoftSamVoice.ROBO_6: return 100
            case MicrosoftSamVoice.SAM: return 100
            case _: raise RuntimeError(f'Unknown MicrosoftSamVoice value: \"{self}\"')

    @property
    def speed(self) -> int:
        match self:
            case MicrosoftSamVoice.ADULT_FEMALE_1: return 150
            case MicrosoftSamVoice.ADULT_FEMALE_2: return 150
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER: return 170
            case MicrosoftSamVoice.ADULT_MALE_1: return 150
            case MicrosoftSamVoice.ADULT_MALE_2: return 150
            case MicrosoftSamVoice.ADULT_MALE_3: return 150
            case MicrosoftSamVoice.ADULT_MALE_4: return 150
            case MicrosoftSamVoice.ADULT_MALE_5: return 150
            case MicrosoftSamVoice.ADULT_MALE_6: return 120
            case MicrosoftSamVoice.ADULT_MALE_7: return 150
            case MicrosoftSamVoice.ADULT_MALE_8: return 150
            case MicrosoftSamVoice.ADULT_MALE_WHISPER: return 170
            case MicrosoftSamVoice.BONZI_BUDDY: return 157
            case MicrosoftSamVoice.MARY: return 170
            case MicrosoftSamVoice.MARY_HALL: return 157
            case MicrosoftSamVoice.MARY_SPACE: return 157
            case MicrosoftSamVoice.MARY_STADIUM: return 157
            case MicrosoftSamVoice.MARY_TELEPHONE: return 170
            case MicrosoftSamVoice.MIKE: return 170
            case MicrosoftSamVoice.MIKE_HALL: return 170
            case MicrosoftSamVoice.MIKE_SPACE: return 170
            case MicrosoftSamVoice.MIKE_STADIUM: return 170
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 170
            case MicrosoftSamVoice.ROBO_1: return 130
            case MicrosoftSamVoice.ROBO_2: return 130
            case MicrosoftSamVoice.ROBO_3: return 170
            case MicrosoftSamVoice.ROBO_4: return 170
            case MicrosoftSamVoice.ROBO_5: return 130
            case MicrosoftSamVoice.ROBO_6: return 130
            case MicrosoftSamVoice.SAM: return 150
            case _: raise RuntimeError(f'Unknown MicrosoftSamVoice value: \"{self}\"')
