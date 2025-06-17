from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType


@dataclass(frozen = True)
class SuperTriviaRecurringEvent(RecurringEvent):
    twitchChannel: str
    twitchChannelId: str

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.SUPER_TRIVIA
