from typing import Any

from .crowdControlSteps import CrowdControlSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class CrowdControlWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = CrowdControlSteps()
        self.__bits: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.CROWD_CONTROL

    def getSteps(self) -> CrowdControlSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__bits=}'

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

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

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }