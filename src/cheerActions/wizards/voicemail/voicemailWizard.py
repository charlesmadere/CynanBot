from typing import Any, Final

from .voicemailStep import VoicemailStep
from .voicemailSteps import VoicemailSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class VoicemailWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps: Final[VoicemailSteps] = VoicemailSteps()
        self.__bits: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.VOICEMAIL

    @property
    def currentStep(self) -> VoicemailStep:
        return self.__steps.currentStep

    def printOut(self) -> str:
        return f'{self.__bits=}'

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    @property
    def steps(self) -> VoicemailSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'cheerActionType': self.cheerActionType,
            'currentStep': self.currentStep,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
