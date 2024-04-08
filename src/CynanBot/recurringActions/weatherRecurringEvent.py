from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringEvent import RecurringEvent
from CynanBot.recurringActions.recurringEventType import RecurringEventType
from CynanBot.weather.weatherReport import WeatherReport


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

    def getEventType(self) -> RecurringEventType:
        return RecurringEventType.WEATHER

    def getWeatherReport(self) -> WeatherReport:
        return self.__weatherReport

    def isAlertsOnly(self) -> bool:
        return self.__alertsOnly

    def toDictionary(self) -> dict[str, Any]:
        return {
            'alertsOnly': self.__alertsOnly,
            'eventType': self.getEventType(),
            'twitchChannel': self.getTwitchChannel(),
            'twitchChannelId': self.getTwitchChannelId(),
            'weatherReport': self.getWeatherReport()
        }
