from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class SuperTriviaRecurringEvent(RecurringEvent):
    twitchChannelId: str
    twitchUser: UserInterface

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.SUPER_TRIVIA

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchUser(self) -> UserInterface:
        return self.twitchUser
