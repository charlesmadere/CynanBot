from abc import abstractmethod

from ..crowdControlCheerAction import CrowdControlCheerAction
from ..crowdControlCheerActionType import CrowdControlCheerActionType
from ...cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...cheerActionType import CheerActionType
from ....misc import utils as utils


class ButtonPressCheerAction(CrowdControlCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        twitchChannelId: str
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.CROWD_CONTROL

    @abstractmethod
    @property
    def crowdControlCheerActionType(self) -> CrowdControlCheerActionType:
        return CrowdControlCheerActionType.BUTTON_PRESS

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, crowdControlActionType={self.crowdControlCheerActionType}'
