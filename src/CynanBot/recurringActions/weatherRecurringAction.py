from typing import Optional

import misc.utils as utils
from recurringActions.recurringAction import RecurringAction
from recurringActions.recurringActionType import RecurringActionType


class WeatherRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        alertsOnly: bool = True,
        minutesBetween: Optional[int] = None
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            minutesBetween = minutesBetween
        )

        if not utils.isValidBool(alertsOnly):
            raise ValueError(f'alertsOnly argument is malformed: \"{alertsOnly}\"')

        self.__alertsOnly: bool = alertsOnly

    def getActionType(self) -> RecurringActionType:
        return RecurringActionType.WEATHER

    def isAlertsOnly(self) -> bool:
        return self.__alertsOnly
