from .crowdControlCheerActionType import CrowdControlCheerActionType
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class CrowdControlCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        crowdControlCheerActionType: CrowdControlCheerActionType,
        bits: int,
        gigaShuffleChance: int | None,
        twitchChannelId: str
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if not isinstance(crowdControlCheerActionType, CrowdControlCheerActionType):
            raise TypeError(f'crowdControlCheerActionType argument is malformed: \"{crowdControlCheerActionType}\"')
        elif gigaShuffleChance is not None and not utils.isValidInt(gigaShuffleChance):
            raise TypeError(f'gigaShuffleChance argument is malformed: \"{gigaShuffleChance}\"')
        elif gigaShuffleChance is not None and (gigaShuffleChance < 0 or gigaShuffleChance > 100):
            raise ValueError(f'gigaShuffleChance argument is out of bounds: {gigaShuffleChance}')

        self.__crowdControlCheerActionType: CrowdControlCheerActionType = crowdControlCheerActionType
        self.__gigaShuffleChance: int | None = gigaShuffleChance

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.CROWD_CONTROL

    @property
    def crowdControlCheerActionType(self) -> CrowdControlCheerActionType:
        return self.__crowdControlCheerActionType

    @property
    def gigaShuffleChance(self) -> int | None:
        return self.__gigaShuffleChance

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, crowdControlActionType={self.__crowdControlCheerActionType}, gigaShuffleChance={self.__gigaShuffleChance}'
