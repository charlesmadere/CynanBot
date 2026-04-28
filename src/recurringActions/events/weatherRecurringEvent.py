from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...users.userInterface import UserInterface
from ...weather.weatherReport import WeatherReport


@dataclass(frozen = True, slots = True)
class WeatherRecurringEvent(RecurringEvent):
    alertsOnly: bool
    twitchChannelId: str
    twitchUser: UserInterface
    weatherReport: WeatherReport

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.WEATHER

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchUser(self) -> UserInterface:
        return self.twitchUser
