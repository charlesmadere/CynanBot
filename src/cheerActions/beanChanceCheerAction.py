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
        randomChance: int,
        actionId: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            isEnable = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            actionId = actionId,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidInt(randomChance):
            raise TypeError(f'randomChance argument is malformed: \"{randomChance}\"')
        elif randomChance < 0 or randomChance > 100:
            raise ValueError(f'randomChance argument is out of bounds: {randomChance}')

        self.__randomChance: int = randomChance

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.BEAN_CHANCE

    @property
    def randomChance(self) -> int:
        return self.__randomChance
