from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class BeanChanceCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        randomChance: int,
        twitchChannelId: str,
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidInt(randomChance):
            raise TypeError(f'randomChance argument is malformed: \"{randomChance}\"')
        elif randomChance < 0 or randomChance > 100:
            raise ValueError(f'randomChance argument is out of bounds: {randomChance}')

        self.__randomChance: Final[int] = randomChance

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.BEAN_CHANCE

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, randomChance={self.__randomChance}'

    @property
    def randomChance(self) -> int:
        return self.__randomChance
