from .microsoftSamVoiceMapperInterface import MicrosoftSamVoiceMapperInterface
from .models.microsoftSamVoice import MicrosoftSamVoice
from .models.microsoftSamVoiceData import MicrosoftSamVoiceData


class MicrosoftSamVoiceMapper(MicrosoftSamVoiceMapperInterface):

    def data(self, voice: MicrosoftSamVoice) -> MicrosoftSamVoiceData:
        if not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case MicrosoftSamVoice.ADULT_FEMALE_1:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Female #1, American English (TruVoice)',
                    pitch = '208',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_FEMALE_2:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Female #2, American English (TruVoice)',
                    pitch = '152',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_1:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #1, American English (TruVoice)',
                    pitch = '85',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_2:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #2, American English (TruVoice)',
                    pitch = '50',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_3:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #3, American English (TruVoice)',
                    pitch = '125',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_4:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #4, American English (TruVoice)',
                    pitch = '73',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_5:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #5, American English (TruVoice)',
                    pitch = '129',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_6:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #6, American English (TruVoice)',
                    pitch = '89',
                    speed = '120'
                )
            case MicrosoftSamVoice.ADULT_MALE_7:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #7, American English (TruVoice)',
                    pitch = '117',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_MALE_8:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #8, American English (TruVoice)',
                    pitch = '203',
                    speed = '150'
                )
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER:
                return MicrosoftSamVoiceData(
                    voice = 'Female Whisper',
                    pitch = '169',
                    speed = '170'
                )
            case MicrosoftSamVoice.ADULT_MALE_WHISPER:
                return MicrosoftSamVoiceData(
                    voice = 'Male Whisper',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.MARY:
                return MicrosoftSamVoiceData(
                    voice = 'Mary',
                    pitch = '169',
                    speed = '170'
                )
            case MicrosoftSamVoice.MARY_TELEPHONE:
                return MicrosoftSamVoiceData(
                    voice = 'Mary (for Telephone)',
                    pitch = '169',
                    speed = '170'
                )
            case MicrosoftSamVoice.MARY_HALL:
                return MicrosoftSamVoiceData(
                    voice = 'Mary in Hall',
                    pitch = '169',
                    speed = '157'
                )
            case MicrosoftSamVoice.MARY_SPACE:
                return MicrosoftSamVoiceData(
                    voice = 'Mary in Space',
                    pitch = '169',
                    speed = '157'
                )
            case MicrosoftSamVoice.MARY_STADIUM:
                return MicrosoftSamVoiceData(
                    voice = 'Mary in Stadium',
                    pitch = '169',
                    speed = '157'
                )
            case MicrosoftSamVoice.MIKE:
                return MicrosoftSamVoiceData(
                    voice = 'Mike',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.MIKE_TELEPHONE:
                return MicrosoftSamVoiceData(
                    voice = 'Mike (for Telephone)',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.MIKE_HALL:
                return MicrosoftSamVoiceData(
                    voice = 'Mike in Hall',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.MIKE_SPACE:
                return MicrosoftSamVoiceData(
                    voice = 'Mike in Space',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.MIKE_STADIUM:
                return MicrosoftSamVoiceData(
                    voice = 'Mike in Stadium',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.ROBO_1:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft One',
                    pitch = '75',
                    speed = '130'
                )
            case MicrosoftSamVoice.ROBO_2:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft Two',
                    pitch = '120',
                    speed = '130'
                )
            case MicrosoftSamVoice.ROBO_3:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft Three',
                    pitch = '113',
                    speed = '170'
                )
            case MicrosoftSamVoice.ROBO_4:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft Four',
                    pitch = '169',
                    speed = '170'
                )
            case MicrosoftSamVoice.ROBO_5:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft Five',
                    pitch = '120',
                    speed = '130'
                )
            case MicrosoftSamVoice.ROBO_6:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft Six',
                    pitch = '100',
                    speed = '130'
                )
            case MicrosoftSamVoice.SAM:
                return MicrosoftSamVoiceData(
                    voice = 'Sam',
                    pitch = '100',
                    speed = '150'
                )
            case MicrosoftSamVoice.BONZI_BUDDY:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #2, American English (TruVoice)',
                    pitch = '140',
                    speed = '157'
                )
            case _: raise RuntimeError(f'voice is an unknown value: \"{voice}\"')
