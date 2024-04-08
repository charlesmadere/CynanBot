from typing import Any

from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class SuperTriviaRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        minutesBetween: int | None = None
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween
        )

    def getActionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionType': self.getActionType(),
            'enabled': self.isEnabled(),
            'minutesBetween': self.getMinutesBetween(),
            'twitchChannel': self.getTwitchChannel(),
            'twitchChannelId': self.getTwitchChannelId()
        }
