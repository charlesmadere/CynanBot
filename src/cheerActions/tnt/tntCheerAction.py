import locale

from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ..cheerActionType import CheerActionType
from ...misc import utils as utils


class TntCheerAction(AbsCheerAction):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        durationSeconds: int,
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

        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidInt(maxTimeoutChatters):
            raise TypeError(f'maxTimeoutChatters argument is malformed: \"{maxTimeoutChatters}\"')
        elif maxTimeoutChatters < 1 or maxTimeoutChatters > utils.getIntMaxSafeSize():
            raise ValueError(f'maxTimeoutChatters argument is out of bounds: {maxTimeoutChatters}')
        elif not utils.isValidInt(minTimeoutChatters):
            raise TypeError(f'minTimeoutChatters argument is malformed: \"{minTimeoutChatters}\"')
        elif minTimeoutChatters < 1 or minTimeoutChatters > utils.getIntMaxSafeSize():
            raise ValueError(f'minTimeoutChatters argument is out of bounds: {minTimeoutChatters}')

        self.__durationSeconds: int = durationSeconds
        self.__maxTimeoutChatters: int = maxTimeoutChatters
        self.__minTimeoutChatters: int = minTimeoutChatters

    @property
    def actionType(self) -> CheerActionType:
        return CheerActionType.TNT

    @property
    def durationSeconds(self) -> int:
        return self.__durationSeconds

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.__durationSeconds, grouping = True)

    @property
    def maxTimeoutChatters(self) -> int:
        return self.__maxTimeoutChatters

    @property
    def minTimeoutChatters(self) -> int:
        return self.__minTimeoutChatters

    def printOut(self) -> str:
        return f'isEnabled={self.isEnabled}, streamStatusRequirement={self.streamStatusRequirement}, actionType={self.actionType}, bits={self.bits}, durationSeconds={self.__durationSeconds}, maxTimeoutChatters={self.__maxTimeoutChatters}, minTimeoutChatters={self.__minTimeoutChatters}'
