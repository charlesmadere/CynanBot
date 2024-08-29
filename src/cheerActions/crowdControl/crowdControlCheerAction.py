from .crowdControlCheerActionType import CrowdControlCheerActionType
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType


class CrowdControlCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        crowdControlCheerActionType: CrowdControlCheerActionType,
        bits: int,
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

        self.__crowdControlCheerActionType: CrowdControlCheerActionType = crowdControlCheerActionType

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.CROWD_CONTROL

    @property
    def crowdControlCheerActionType(self) -> CrowdControlCheerActionType:
        return self.__crowdControlCheerActionType

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, crowdControlActionType={self.__crowdControlCheerActionType}'
