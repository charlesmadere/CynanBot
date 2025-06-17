from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...weather.weatherReport import WeatherReport


@dataclass(frozen = True)
class WeatherRecurringEvent(RecurringEvent):
    alertsOnly: bool
    twitchChannel: str
    twitchChannelId: str
    weatherReport: WeatherReport

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.WEATHER
