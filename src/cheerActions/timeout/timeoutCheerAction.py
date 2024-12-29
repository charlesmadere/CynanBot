import locale

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class TimeoutCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        isRandomChanceEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        durationSeconds: int,
        twitchChannelId: str
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidBool(isRandomChanceEnabled):
            raise TypeError(f'isRandomChanceEnabled argument is malformed: \"{isRandomChanceEnabled}\"')
        elif not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')

        self.__isRandomChanceEnabled: bool = isRandomChanceEnabled
        self.__durationSeconds: int = durationSeconds

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.TIMEOUT

    @property
    def durationSeconds(self) -> int:
        return self.__durationSeconds

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.__durationSeconds, grouping = True)

    @property
    def isRandomChanceEnabled(self) -> bool:
        return self.__isRandomChanceEnabled

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, isRandomChanceEnabled={self.isRandomChanceEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, durationSeconds={self.__durationSeconds}'
