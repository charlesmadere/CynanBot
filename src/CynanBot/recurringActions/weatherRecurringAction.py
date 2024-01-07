from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType


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

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'actionType': self.getActionType(),
            'alertsOnly': self.__alertsOnly,
            'enabled': self.isEnabled(),
            'minutesBetween': self.getMinutesBetween(),
            'twitchChannel': self.getTwitchChannel()
        }
