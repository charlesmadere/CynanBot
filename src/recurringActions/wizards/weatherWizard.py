from typing import Any

from .absWizard import AbsWizard
from .weatherSteps import WeatherSteps
from ..recurringActionType import RecurringActionType
from ...misc import utils as utils


class WeatherWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = WeatherSteps()
        self.__minutesBetween: int | None = None
        self.__alertsOnly: bool | None = None

    def getSteps(self) -> WeatherSteps:
        return self.__steps

    def printOut(self) -> str:
        return f'{self.__minutesBetween=},{self.__alertsOnly=}'

    @property
    def recurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WEATHER

    def requireAlertsOnly(self) -> bool:
        alertsOnly = self.__alertsOnly

        if alertsOnly is None:
            raise ValueError(f'alertsOnly value has not been set: ({self=})')

        return alertsOnly

    def requireMinutesBetween(self) -> int:
        minutesBetween = self.__minutesBetween

        if minutesBetween is None:
            raise ValueError(f'minutesBetween value has not been set: ({self=})')

        return minutesBetween

    def setAlertsOnly(self, alertsOnly: bool):
        if not utils.isValidBool(alertsOnly):
            raise TypeError(f'alertsOnly argument is malformed: \"{alertsOnly}\"')

        self.__alertsOnly = alertsOnly

    def setMinutesBetween(self, minutesBetween: int):
        if not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize():
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')
        elif minutesBetween < self.recurringActionType.minimumRecurringActionTimingMinutes:
            raise ValueError(f'minutesBetween argument is below the minimum requirement: {minutesBetween}')

        self.__minutesBetween = minutesBetween

    def toDictionary(self) -> dict[str, Any]:
        return {
            'minutesBetween': self.__minutesBetween,
            'alertsOnly': self.__alertsOnly,
            'recurringActionType': self.recurringActionType,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId
        }
