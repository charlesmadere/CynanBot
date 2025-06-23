from typing import Any, Final

from .weatherStep import WeatherStep
from .weatherSteps import WeatherSteps
from ..absWizard import AbsWizard
from ...actions.recurringActionType import RecurringActionType
from ....misc import utils as utils


class WeatherWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        self.__steps: Final[WeatherSteps] = WeatherSteps()
        self.__minutesBetween: int | None = None
        self.__alertsOnly: bool | None = None

    @property
    def currentStep(self) -> WeatherStep:
        return self.__steps.currentStep

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

    @property
    def steps(self) -> WeatherSteps:
        return self.__steps

    def toDictionary(self) -> dict[str, Any]:
        return {
            'alertsOnly': self.__alertsOnly,
            'currentStep': self.currentStep,
            'minutesBetween': self.__minutesBetween,
            'recurringActionType': self.recurringActionType,
            'steps': self.__steps,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
