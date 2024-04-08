from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class WeatherRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        alertsOnly: bool = True,
        minutesBetween: int | None = None
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween
        )

        if not utils.isValidBool(alertsOnly):
            raise TypeError(f'alertsOnly argument is malformed: \"{alertsOnly}\"')

        self.__alertsOnly: bool = alertsOnly

    def getActionType(self) -> RecurringActionType:
        return RecurringActionType.WEATHER

    def isAlertsOnly(self) -> bool:
        return self.__alertsOnly

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionType': self.getActionType(),
            'alertsOnly': self.__alertsOnly,
            'enabled': self.isEnabled(),
            'minutesBetween': self.getMinutesBetween(),
            'twitchChannel': self.getTwitchChannel(),
            'twitchChannelId': self.getTwitchChannelId()
        }
