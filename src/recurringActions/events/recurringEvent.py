from abc import ABC, abstractmethod

from .recurringEventType import RecurringEventType
from ...users.userInterface import UserInterface


class RecurringEvent(ABC):

    @property
    @abstractmethod
    def eventType(self) -> RecurringEventType:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchUser(self) -> UserInterface:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.getTwitchUser().handle
