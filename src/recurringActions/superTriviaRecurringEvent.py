from typing import Any

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType


class SuperTriviaRecurringEvent(RecurringEvent):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    def getEventType(self) -> RecurringEventType:
        return RecurringEventType.SUPER_TRIVIA

    def toDictionary(self) -> dict[str, Any]:
        return {
            'eventType': self.getEventType(),
            'twitchChannel': self.getTwitchChannel(),
            'twitchChannelId': self.getTwitchChannelId()
        }
