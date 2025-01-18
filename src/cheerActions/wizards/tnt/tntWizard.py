from typing import Any

from .tntSteps import TntSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class TntWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps: TntSteps = TntSteps()
        self.__bits: int | None = None
        self.__durationSeconds: int | None = None
        self.__maxTimeoutChatters: int | None = None
        self.__minTimeoutChatters: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.TNT

    def getSteps(self) -> TntSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__durationSeconds=}, {self.__maxTimeoutChatters=}, {self.__minTimeoutChatters=}'

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

    def requireMaxTimeoutChatters(self) -> int:
        maxTimeoutChatters = self.__maxTimeoutChatters

        if maxTimeoutChatters is None:
            raise ValueError(f'maxTimeoutChatters value has not been set: ({self=})')

        return maxTimeoutChatters

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

    def setDurationSeconds(self, durationSeconds: int):
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')

        self.__durationSeconds = durationSeconds

    def setMaxTimeoutChatters(self, maxTimeoutChatters: int):
        if not utils.isValidInt(maxTimeoutChatters):
            raise TypeError(f'maxTimeoutChatters argument is malformed: \"{maxTimeoutChatters}\"')

        self.__maxTimeoutChatters = maxTimeoutChatters

    def setMinTimeoutChatters(self, minTimeoutChatters: int):
        if not utils.isValidInt(minTimeoutChatters):
            raise TypeError(f'minTimeoutChatters argument is malformed: \"{minTimeoutChatters}\"')

        self.__minTimeoutChatters = minTimeoutChatters

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'cheerActionType': self.cheerActionType,
            'durationSeconds': self.__durationSeconds,
            'maxTimeoutChatters': self.__maxTimeoutChatters,
            'minTimeoutChatters': self.__minTimeoutChatters,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
