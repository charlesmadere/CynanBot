from typing import Any

from .gameShuffleSteps import GameShuffleSteps
from ..absWizard import AbsWizard
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class GameShuffleWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = GameShuffleSteps()
        self.__bits: int | None = None
        self.__superShuffleChance: int | None = None

    @property
    def cheerActionType(self) -> CheerActionType:
        return CheerActionType.GAME_SHUFFLE

    def getSteps(self) -> GameShuffleSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__bits=}, {self.__superShuffleChance}'

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

    def setSuperShuffleChance(self, superShuffleChance: int):
        if not utils.isValidInt(superShuffleChance):
            raise TypeError(f'superShuffleChance argument is malformed: \"{superShuffleChance}\"')
        elif superShuffleChance < 0 or superShuffleChance > 100:
            raise ValueError(f'superShuffleChance argument is out of bounds: {superShuffleChance}')

        self.__superShuffleChance = superShuffleChance

    @property
    def superShuffleChance(self) -> int | None:
        return self.__superShuffleChance

    def toDictionary(self) -> dict[str, Any]:
        return {
            'bits': self.__bits,
            'steps': self.__steps,
            'superShuffleChance': self.__superShuffleChance,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
