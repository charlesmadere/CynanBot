from typing import Any

from .recurringAction import RecurringAction
from .recurringActionType import RecurringActionType


class SuperTriviaRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        minutesBetween: int | None = None,
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween,
        )

    @property
    def actionType(self) -> RecurringActionType:
        return RecurringActionType.SUPER_TRIVIA

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionType': self.actionType,
            'enabled': self.isEnabled,
            'minutesBetween': self.minutesBetween,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
