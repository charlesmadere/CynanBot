from typing import Any

from .airStrikeStep import AirStrikeStep
from .airStrikeSteps import AirStrikeSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class AirStrikeWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps: AirStrikeSteps = AirStrikeSteps()
        self.__bits: int | None = None
        self.__maxDurationSeconds: int | None = None
        self.__minDurationSeconds: int | None = None
        self.__maxTimeoutChatters: int | None = None
        self.__minTimeoutChatters: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.AIR_STRIKE

    @property
    def currentStep(self) -> AirStrikeStep:
        return self.__steps.currentStep

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__maxDurationSeconds=}, {self.__minDurationSeconds=}, {self.__maxTimeoutChatters=}, {self.__minTimeoutChatters=}'

    def requireBits(self) -> int:
        bits = self.__bits

        if bits is None:
            raise ValueError(f'bits value has not been set: ({self=})')

        return bits

    def requireMaxDurationSeconds(self) -> int:
        maxDurationSeconds = self.__maxDurationSeconds

        if maxDurationSeconds is None:
            raise ValueError(f'maxDurationSeconds value has not been set: ({self=})')

        return maxDurationSeconds

    def requireMaxTimeoutChatters(self) -> int:
        maxTimeoutChatters = self.__maxTimeoutChatters

        if maxTimeoutChatters is None:
            raise ValueError(f'maxTimeoutChatters value has not been set: ({self=})')

        return maxTimeoutChatters

    def requireMinDurationSeconds(self) -> int:
        minDurationSeconds = self.__minDurationSeconds

        if minDurationSeconds is None:
            raise ValueError(f'minDurationSeconds value has not been set: ({self=})')

        return minDurationSeconds

    def requireMinTimeoutChatters(self) -> int:
        minTimeoutChatters = self.__minTimeoutChatters

        if minTimeoutChatters is None:
            raise ValueError(f'minTimeoutChatters value has not been set: ({self=})')

        return minTimeoutChatters

    def setBits(self, bits: int):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')

        self.__bits = bits

    def setMaxDurationSeconds(self, maxDurationSeconds: int):
        if not utils.isValidInt(maxDurationSeconds):
            raise TypeError(f'maxDurationSeconds argument is malformed: \"{maxDurationSeconds}\"')
        elif maxDurationSeconds < 1 or maxDurationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'maxDurationSeconds argument is out of bounds: {maxDurationSeconds}')

        self.__maxDurationSeconds = maxDurationSeconds

    def setMaxTimeoutChatters(self, maxTimeoutChatters: int):
        if not utils.isValidInt(maxTimeoutChatters):
            raise TypeError(f'maxTimeoutChatters argument is malformed: \"{maxTimeoutChatters}\"')
        elif self.__minTimeoutChatters is not None and maxTimeoutChatters < self.__minTimeoutChatters:
            raise ValueError(f'maxTimeoutChatters argument can\'t be less than minTimeoutChatters ({maxTimeoutChatters=}) ({self.__minTimeoutChatters=})')

        self.__maxTimeoutChatters = maxTimeoutChatters

    def setMinDurationSeconds(self, minDurationSeconds: int):
        if not utils.isValidInt(minDurationSeconds):
            raise TypeError(f'minDurationSeconds argument is malformed: \"{minDurationSeconds}\"')
        elif minDurationSeconds < 1 or minDurationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'minDurationSeconds argument is out of bounds: {minDurationSeconds}')

        self.__minDurationSeconds = minDurationSeconds

    def setMinTimeoutChatters(self, minTimeoutChatters: int):
        if not utils.isValidInt(minTimeoutChatters):
            raise TypeError(f'minTimeoutChatters argument is malformed: \"{minTimeoutChatters}\"')
        elif self.__maxTimeoutChatters is not None and minTimeoutChatters > self.__maxTimeoutChatters:
            raise ValueError(f'minTimeoutChatters argument can\'t be more than maxTimeoutChatters ({minTimeoutChatters=}) ({self.__maxTimeoutChatters=})')

        self.__minTimeoutChatters = minTimeoutChatters

    @property
    def steps(self) -> AirStrikeSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'cheerActionType': self.cheerActionType,
            'currentStep': self.currentStep,
            'maxDurationSeconds': self.__maxDurationSeconds,
            'minDurationSeconds': self.__minDurationSeconds,
            'maxTimeoutChatters': self.__maxTimeoutChatters,
            'minTimeoutChatters': self.__minTimeoutChatters,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
