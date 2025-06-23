from typing import Any, Final

from .timeoutStep import TimeoutStep
from .timeoutSteps import TimeoutSteps
from ..absWizard import AbsWizard
from ...cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...cheerActionType import CheerActionType
from ...timeout.timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from ....misc import utils as utils


class TimeoutWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps: Final[TimeoutSteps] = TimeoutSteps()
        self.__randomChanceEnabled: bool | None = None
        self.__streamStatus: CheerActionStreamStatusRequirement | None = None
        self.__bits: int | None = None
        self.__durationSeconds: int | None = None
        self.__targetType: TimeoutCheerActionTargetType | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.TIMEOUT

    @property
    def currentStep(self) -> TimeoutStep:
        return self.__steps.currentStep

    def printOut(self) -> str:
        return f'{self.__randomChanceEnabled=}, {self.__streamStatus=}, {self.__bits=}, {self.__durationSeconds=}'

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def requireDurationSeconds(self) -> int:
        durationSeconds = self.__durationSeconds

        if durationSeconds is None:
            raise ValueError(f'durationSeconds value has not been set: ({self=})')

        return durationSeconds

    def requireRandomChanceEnabled(self) -> bool:
        randomChanceEnabled = self.__randomChanceEnabled

        if randomChanceEnabled is None:
            raise ValueError(f'randomChanceEnabled value has not been set: ({self=})')

        return randomChanceEnabled

    def requireStreamStatus(self) -> CheerActionStreamStatusRequirement:
        streamStatus = self.__streamStatus

        if streamStatus is None:
            raise ValueError(f'streamStatus value has not been set: ({self=})')

        return streamStatus

    def requireTargetType(self) -> TimeoutCheerActionTargetType:
        targetType = self.__targetType

        if targetType is None:
            raise ValueError(f'targetType value has not been set: ({self=})')

        return targetType

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    def setDurationSeconds(self, durationSeconds: int):
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')

        self.__durationSeconds = durationSeconds

    def setRandomChanceEnabled(self, randomChanceEnabled: bool):
        if not utils.isValidBool(randomChanceEnabled):
            raise TypeError(f'randomChanceEnabled argument is malformed: \"{randomChanceEnabled}\"')

        self.__randomChanceEnabled = randomChanceEnabled

    def setStreamStatus(self, streamStatus: CheerActionStreamStatusRequirement):
        if not isinstance(streamStatus, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatus argument is malformed: \"{streamStatus}\"')

        self.__streamStatus = streamStatus

    def setTargetType(self, targetType: TimeoutCheerActionTargetType):
        if not isinstance(targetType, TimeoutCheerActionTargetType):
            raise TypeError(f'targetType argument is malformed: \"{targetType}\"')

        self.__targetType = targetType

    @property
    def steps(self) -> TimeoutSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'cheerActionType': self.cheerActionType,
            'currentStep': self.currentStep,
            'durationSeconds': self.__durationSeconds,
            'randomChanceEnabled': self.__randomChanceEnabled,
            'steps': self.__steps,
            'streamStatus': self.__streamStatus,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
