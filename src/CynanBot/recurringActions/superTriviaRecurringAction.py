from typing import Any, Dict, Optional

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

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'actionType': self.getActionType(),
            'enabled': self.isEnabled(),
            'minutesBetween': self.getMinutesBetween(),
            'twitchChannel': self.getTwitchChannel()
        }
