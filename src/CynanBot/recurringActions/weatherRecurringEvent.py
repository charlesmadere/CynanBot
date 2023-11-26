import misc.utils as utils
from recurringActions.recurringEvent import RecurringEvent
from recurringActions.recurringEventType import RecurringEventType
from weather.weatherReport import WeatherReport


class WeatherRecurringEvent(RecurringEvent):

    def __init__(
        self,
        alertsOnly: bool,
        twitchChannel: str,
        weatherReport: WeatherReport
    ):
        super().__init__(twitchChannel = twitchChannel)

        if not utils.isValidBool(alertsOnly):
            raise ValueError(f'alertsOnly argument is malformed: \"{alertsOnly}\"')
        elif not isinstance(weatherReport, WeatherReport):
            raise ValueError(f'weatherReport argument is malformed: \"{weatherReport}\"')

        self.__alertsOnly: bool = alertsOnly
        self.__weatherReport: WeatherReport = weatherReport

    def getEventType(self) -> RecurringEventType:
        return RecurringEventType.WEATHER

    def getWeatherReport(self) -> WeatherReport:
        return self.__weatherReport

    def isAlertsOnly(self) -> bool:
        return self.__alertsOnly
