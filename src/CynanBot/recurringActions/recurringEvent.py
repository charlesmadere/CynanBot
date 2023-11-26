from abc import ABC, abstractmethod

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
