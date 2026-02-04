from typing import Any, Final

from .recurringAction import RecurringAction
from .recurringActionType import RecurringActionType
from ...misc import utils as utils


class WeatherRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        alertsOnly: bool = True,
        minutesBetween: int | None = None,
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween,
        )

        if not utils.isValidBool(alertsOnly):
            raise TypeError(f'alertsOnly argument is malformed: \"{alertsOnly}\"')

        self.__alertsOnly: Final[bool] = alertsOnly

    @property
    def actionType(self) -> RecurringActionType:
        return RecurringActionType.WEATHER

    @property
    def isAlertsOnly(self) -> bool:
        return self.__alertsOnly

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionType': self.actionType,
            'alertsOnly': self.__alertsOnly,
            'enabled': self.isEnabled,
            'minutesBetween': self.minutesBetween,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
