from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class AdgeCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        adgeLengthSeconds: int,
        bits: int,
        twitchChannelId: str,
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidInt(adgeLengthSeconds):
            raise TypeError(f'adgeLengthSeconds argument is malformed: \"{adgeLengthSeconds}\"')
        elif adgeLengthSeconds < 1 or adgeLengthSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'adgeLengthSeconds argument is out of bounds: {adgeLengthSeconds}')

        self.__adgeLengthSeconds: Final[int] = adgeLengthSeconds

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.ADGE

    @property
    def adgeLengthSeconds(self) -> int:
        return self.__adgeLengthSeconds

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, adgeLengthSeconds={self.__adgeLengthSeconds}, bits={self.bits}'
