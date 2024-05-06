from dataclasses import dataclass
from datetime import tzinfo

from CynanBot.openWeather.openWeatherAlert import OpenWeatherAlert
from CynanBot.openWeather.openWeatherDay import OpenWeatherDay
from CynanBot.openWeather.openWeatherMoment import OpenWeatherMoment


@dataclass(frozen = True)
class OpenWeatherReport():
    latitude: float
    longitude: float
    alerts: list[OpenWeatherAlert] | None
    days: list[OpenWeatherDay]
    current: OpenWeatherMoment
    timeZone: tzinfo
