from typing import Any

from .timeoutSteps import TimeoutSteps
from ..absWizard import AbsWizard
from ...cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...cheerActionType import CheerActionType
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

        self.__steps = TimeoutSteps()
        self.__randomChanceEnabled: bool | None = None
        self.__targetsRandomActiveChatter: bool | None = None
        self.__streamStatus: CheerActionStreamStatusRequirement | None = None
        self.__bits: int | None = None
        self.__durationSeconds: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.TIMEOUT

    def getSteps(self) -> TimeoutSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__randomChanceEnabled=}, {self.__targetsRandomActiveChatter=}, {self.__streamStatus=}, {self.__bits=}, {self.__durationSeconds=}'

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

    def requireTargetsRandomActiveChatter(self) -> bool:
        targetsRandomActiveChatter = self.__targetsRandomActiveChatter

        if targetsRandomActiveChatter is None:
            raise ValueError(f'targetsRandomActiveChatter value has not been set: ({self=})')

        return targetsRandomActiveChatter

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

    def setTargetsRandomActiveChatter(self, targetsRandomActiveChatter: bool):
        if not utils.isValidBool(targetsRandomActiveChatter):
            raise TypeError(f'targetsRandomActiveChatter argument is malformed: \"{targetsRandomActiveChatter}\"')

        self.__targetsRandomActiveChatter = targetsRandomActiveChatter

    def setStreamStatus(self, streamStatus: CheerActionStreamStatusRequirement):
        if not isinstance(streamStatus, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatus argument is malformed: \"{streamStatus}\"')

        self.__streamStatus = streamStatus

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'cheerActionType': self.cheerActionType,
            'durationSeconds': self.__durationSeconds,
            'randomChanceEnabled': self.__randomChanceEnabled,
            'steps': self.__steps,
            'streamStatus': self.__streamStatus,
            'targetsRandomActiveChatter': self.__targetsRandomActiveChatter,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
