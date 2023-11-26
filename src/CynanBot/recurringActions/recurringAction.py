from abc import ABC, abstractmethod
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class RecurringAction(ABC):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        minutesBetween: Optional[int] = None
    ):
        if not utils.isValidBool(enabled):
            raise ValueError(f'enabled argument is malformed: \"{enabled}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif minutesBetween is not None and not utils.isValidInt(minutesBetween):
            raise ValueError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween is not None and (minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize()):
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')

        self.__enabled: bool = enabled
        self.__twitchChannel: str = twitchChannel
        self.__minutesBetween: Optional[int] = minutesBetween

    @abstractmethod
    def getActionType(self) -> RecurringActionType:
        pass

    def getMinutesBetween(self) -> Optional[int]:
        return self.__minutesBetween

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def hasMinutesBetween(self) -> bool:
        return utils.isValidInt(self.__minutesBetween)

    def isEnabled(self) -> bool:
        return self.__enabled
