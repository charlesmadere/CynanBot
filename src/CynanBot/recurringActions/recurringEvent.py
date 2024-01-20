from abc import ABC, abstractmethod
from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringEventType import RecurringEventType


class RecurringEvent(ABC):

    def __init__(self, twitchChannel: str):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel

    @abstractmethod
    def getEventType(self) -> RecurringEventType:
        pass

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'eventType': self.getEventType(),
            'twitchChannel': self.__twitchChannel
        }
