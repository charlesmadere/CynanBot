from typing import Optional

from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class SuperTriviaRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        minutesBetween: Optional[int] = None
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            minutesBetween = minutesBetween
        )

    def getActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA
