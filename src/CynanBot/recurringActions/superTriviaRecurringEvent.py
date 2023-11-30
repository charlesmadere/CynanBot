from CynanBot.recurringActions.recurringEvent import RecurringEvent
from CynanBot.recurringActions.recurringEventType import RecurringEventType


class SuperTriviaRecurringEvent(RecurringEvent):

    def __init__(self, twitchChannel: str):
        super().__init__(twitchChannel = twitchChannel)

    def getEventType(self) -> RecurringEventType:
        return RecurringEventType.SUPER_TRIVIA
