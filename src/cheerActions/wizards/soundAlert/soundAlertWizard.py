from typing import Any, Final

from .soundAlertStep import SoundAlertStep
from .soundAlertSteps import SoundAlertSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class SoundAlertWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__steps: Final[SoundAlertSteps] = SoundAlertSteps()
        self.__bits: int | None = None
        self.__directory: str | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.SOUND_ALERT

    @property
    def currentStep(self) -> SoundAlertStep:
        return self.__steps.currentStep

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__directory=}'

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def requireDirectory(self) -> str:
        directory = self.__directory

        if directory is None:
            raise ValueError(f'directory value has not been set: ({self=})')

        return directory

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    def setDirectory(self, directory: str):
        if not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__directory = directory

    @property
    def steps(self) -> SoundAlertSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'cheerActionType': self.cheerActionType,
            'currentStep': self.currentStep,
            'directory': self.__directory,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
