from .models.microsoftSamVoiceData import MicrosoftSamVoiceData
from .microsoftSamVoiceMapperInterface import MicrosoftSamVoiceMapperInterface
from .models.microsoftSamVoice import MicrosoftSamVoice
from ..misc import utils as utils


class MicrosoftSamVoiceMapper(MicrosoftSamVoiceMapperInterface):

    def data(self, voice: MicrosoftSamVoice) -> MicrosoftSamVoiceData:
        if not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case MicrosoftSamVoice.ADULT_MALE_2:
                return MicrosoftSamVoiceData(
                    voice = 'Adult Male #2, American English (TruVoice)',
                    pitch = '140',
                    speed = '157'
                )
            case MicrosoftSamVoice.SAM:
                return MicrosoftSamVoiceData(
                    voice = 'Sam',
                    pitch = '100',
                    speed = '150'
                )
            case MicrosoftSamVoice.ROBO_4:
                return MicrosoftSamVoiceData(
                    voice = 'RoboSoft Four',
                    pitch = '169',
                    speed = '170'
                )
            case _: raise RuntimeError(f'voice is an unknown value: \"{voice}\"')
