from abc import ABC, abstractmethod

from .recurringEventType import RecurringEventType


class RecurringEvent(ABC):

    @property
    @abstractmethod
    def eventType(self) -> RecurringEventType:
        pass

    @property
    @abstractmethod
    def twitchChannel(self) -> str:
        pass

    @property
    @abstractmethod
    def twitchChannelId(self) -> str:
        pass
