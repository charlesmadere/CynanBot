from typing import Any

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...misc import utils as utils
from ...weather.weatherReport import WeatherReport


class WeatherRecurringEvent(RecurringEvent):

    def __init__(
        self,
        alertsOnly: bool,
        twitchChannel: str,
        twitchChannelId: str,
        weatherReport: WeatherReport
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidBool(alertsOnly):
            raise TypeError(f'alertsOnly argument is malformed: \"{alertsOnly}\"')
        elif not isinstance(weatherReport, WeatherReport):
            raise TypeError(f'weatherReport argument is malformed: \"{weatherReport}\"')

        self.__alertsOnly: bool = alertsOnly
        self.__weatherReport: WeatherReport = weatherReport

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.WEATHER

    @property
    def isAlertsOnly(self) -> bool:
        return self.__alertsOnly

    def toDictionary(self) -> dict[str, Any]:
        return {
            'alertsOnly': self.__alertsOnly,
            'eventType': self.eventType,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
            'weatherReport': self.weatherReport
        }

    @property
    def weatherReport(self) -> WeatherReport:
        return self.__weatherReport
