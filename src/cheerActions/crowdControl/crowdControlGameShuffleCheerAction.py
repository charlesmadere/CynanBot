from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class CrowdControlGameShuffleCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        gigaShuffleChance: int | None,
        twitchChannelId: str,
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if gigaShuffleChance is not None and not utils.isValidInt(gigaShuffleChance):
            raise TypeError(f'gigaShuffleChance argument is malformed: \"{gigaShuffleChance}\"')
        elif gigaShuffleChance is not None and (gigaShuffleChance < 0 or gigaShuffleChance > 100):
            raise ValueError(f'gigaShuffleChance argument is out of bounds: {gigaShuffleChance}')

        self.__gigaShuffleChance: Final[int | None] = gigaShuffleChance

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.GAME_SHUFFLE

    @property
    def gigaShuffleChance(self) -> int | None:
        return self.__gigaShuffleChance

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, gigaShuffleChance={self.gigaShuffleChance}'
