from abc import ABC, abstractmethod
from typing import Any

from .recurringActionType import RecurringActionType
from ..misc import utils as utils


class RecurringAction(ABC):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        minutesBetween: int | None = None
    ):
        if not utils.isValidBool(enabled):
            raise TypeError(f'enabled argument is malformed: \"{enabled}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif minutesBetween is not None and not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween is not None and (minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize()):
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')

        self.__enabled: bool = enabled
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__minutesBetween: int | None = minutesBetween

    @abstractmethod
    def getActionType(self) -> RecurringActionType:
        pass

    def getMinutesBetween(self) -> int | None:
        return self.__minutesBetween

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def isEnabled(self) -> bool:
        return self.__enabled

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass
