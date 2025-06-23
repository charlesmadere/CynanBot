import locale
from typing import Final

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class AirStrikeCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        maxDurationSeconds: int,
        minDurationSeconds: int,
        maxTimeoutChatters: int,
        minTimeoutChatters: int,
        twitchChannelId: str
    ):
        super().__init__(
            isEnabled = isEnabled,
            streamStatusRequirement = streamStatusRequirement,
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidInt(maxDurationSeconds):
            raise TypeError(f'maxDurationSeconds argument is malformed: \"{maxDurationSeconds}\"')
        elif maxDurationSeconds < 1 or maxDurationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'maxDurationSeconds argument is out of bounds: {maxDurationSeconds}')
        elif not utils.isValidInt(minDurationSeconds):
            raise TypeError(f'minDurationSeconds argument is malformed: \"{minDurationSeconds}\"')
        elif minDurationSeconds < 1 or minDurationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'minDurationSeconds argument is out of bounds: {minDurationSeconds}')
        elif not utils.isValidInt(maxTimeoutChatters):
            raise TypeError(f'maxTimeoutChatters argument is malformed: \"{maxTimeoutChatters}\"')
        elif maxTimeoutChatters < 1 or maxTimeoutChatters > utils.getIntMaxSafeSize():
            raise ValueError(f'maxTimeoutChatters argument is out of bounds: {maxTimeoutChatters}')
        elif not utils.isValidInt(minTimeoutChatters):
            raise TypeError(f'minTimeoutChatters argument is malformed: \"{minTimeoutChatters}\"')
        elif minTimeoutChatters < 1 or minTimeoutChatters > utils.getIntMaxSafeSize():
            raise ValueError(f'minTimeoutChatters argument is out of bounds: {minTimeoutChatters}')

        self.__maxDurationSeconds: Final[int] = maxDurationSeconds
        self.__minDurationSeconds: Final[int] = minDurationSeconds
        self.__maxTimeoutChatters: Final[int] = maxTimeoutChatters
        self.__minTimeoutChatters: Final[int] = minTimeoutChatters

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.AIR_STRIKE

    @property
    def maxDurationSeconds(self) -> int:
        return self.__maxDurationSeconds

    @property
    def maxDurationSecondsStr(self) -> str:
        return locale.format_string("%d", self.__maxDurationSeconds, grouping = True)

    @property
    def maxTimeoutChatters(self) -> int:
        return self.__maxTimeoutChatters

    @property
    def minDurationSeconds(self) -> int:
        return self.__minDurationSeconds

    @property
    def minDurationSecondsStr(self) -> str:
        return locale.format_string("%d", self.__minDurationSeconds, grouping = True)

    @property
    def minTimeoutChatters(self) -> int:
        return self.__minTimeoutChatters

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, maxDurationSeconds={self.__maxDurationSeconds}, minDurationSeconds={self.__minDurationSeconds}, maxTimeoutChatters={self.__maxTimeoutChatters}, minTimeoutChatters={self.__minTimeoutChatters}'
