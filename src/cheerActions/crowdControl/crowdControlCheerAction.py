from abc import abstractmethod

from .crowdControlCheerActionType import CrowdControlCheerActionType
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...misc import utils as utils


class CrowdControlCheerAction(AbsCheerAction):

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

    @abstractmethod
    @property
    def crowdControlCheerActionType(self) -> CrowdControlCheerActionType:
        pass
