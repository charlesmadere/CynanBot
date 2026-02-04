from abc import ABC, abstractmethod
from typing import Any, Final

from .recurringActionType import RecurringActionType
from ...misc import utils as utils


class RecurringAction(ABC):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        minutesBetween: int | None = None,
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

        self.__enabled: Final[bool] = enabled
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__minutesBetween: Final[int | None] = minutesBetween

    @property
    @abstractmethod
    def actionType(self) -> RecurringActionType:
        pass

    @property
    def isEnabled(self) -> bool:
        return self.__enabled

    @property
    def minutesBetween(self) -> int | None:
        return self.__minutesBetween

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass
