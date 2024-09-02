from .absCheerAction import AbsCheerAction
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc import utils as utils


class BeanChanceCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        maximumPerDay: int | None,
        randomChance: int,
        twitchChannelId: str
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if maximumPerDay is not None and not utils.isValidInt(maximumPerDay):
            raise TypeError(f'maximumPerDay argument is malformed: \"{maximumPerDay}\"')
        elif maximumPerDay is not None and (maximumPerDay < 1 or maximumPerDay > utils.getIntMaxSafeSize()):
            raise ValueError(f'maximumPerDay argument is out of bounds: {maximumPerDay}')
        elif not utils.isValidInt(randomChance):
            raise TypeError(f'randomChance argument is malformed: \"{randomChance}\"')
        elif randomChance < 0 or randomChance > 100:
            raise ValueError(f'randomChance argument is out of bounds: {randomChance}')

        self.__maximumPerDay: int | None = maximumPerDay
        self.__randomChance: int = randomChance

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.BEAN_CHANCE

    @property
    def maximumPerDay(self) -> int:
        return self.__maximumPerDay

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, maximumPerDay={self.__maximumPerDay}, randomChance={self.__randomChance}'

    @property
    def randomChance(self) -> int:
        return self.__randomChance
