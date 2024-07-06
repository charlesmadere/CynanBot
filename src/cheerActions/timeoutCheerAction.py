import locale

from .absCheerAction import AbsCheerAction
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc import utils as utils


class TimeoutCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        durationSeconds: int,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            isEnable = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')

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
