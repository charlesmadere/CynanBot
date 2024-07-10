import locale
from abc import ABC, abstractmethod
from typing import Any

from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from ..misc import utils as utils


class AbsCheerAction(ABC):

    def __init__(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        bits: int,
        twitchChannelId: str
    ):
        if not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__isEnabled: bool = isEnabled
        self.__streamStatusRequirement: CheerActionStreamStatusRequirement = streamStatusRequirement
        self.__bits = bits
        self.__twitchChannelId: str = twitchChannelId

    @property
    @abstractmethod
    def actionType(self) -> CheerActionType:
        pass

    @property
    def bits(self) -> int:
        return self.__bits

    @property
    def bitsString(self) -> str:
        return locale.format_string("%d", self.bits, grouping = True)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AbsCheerAction):
            return False

        return self.__bits == other.bits and self.__twitchChannelId == other.twitchChannelId

    def __hash__(self) -> int:
        return hash((self.__bits, self.__twitchChannelId))

    @property
    def isEnabled(self) -> bool:
        return self.__isEnabled

    @abstractmethod
    def printOut(self) -> str:
        pass

    @property
    def streamStatusRequirement(self) -> CheerActionStreamStatusRequirement:
        return self.__streamStatusRequirement

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
