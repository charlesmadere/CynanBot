from typing import Any, Final

from .gameShuffleStep import GameShuffleStep
from .gameShuffleSteps import GameShuffleSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class GameShuffleWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__steps: Final[GameShuffleSteps] = GameShuffleSteps()
        self.__bits: int | None = None
        self.__gigaShuffleChance: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.GAME_SHUFFLE

    @property
    def currentStep(self) -> GameShuffleStep:
        return self.__steps.currentStep

    @property
    def gigaShuffleChance(self) -> int | None:
        return self.__gigaShuffleChance

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__gigaShuffleChance}'

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

    def setGigaShuffleChance(self, gigaShuffleChance: int):
        if not utils.isValidInt(gigaShuffleChance):
            raise TypeError(f'gigaShuffleChance argument is malformed: \"{gigaShuffleChance}\"')
        elif gigaShuffleChance < 0 or gigaShuffleChance > 100:
            raise ValueError(f'gigaShuffleChance argument is out of bounds: {gigaShuffleChance}')

        self.__gigaShuffleChance = gigaShuffleChance

    @property
    def steps(self) -> GameShuffleSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'currentStep': self.currentStep,
            'gigaShuffleChance': self.__gigaShuffleChance,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
