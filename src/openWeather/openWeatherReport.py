from dataclasses import dataclass
from datetime import tzinfo

from .openWeatherAlert import OpenWeatherAlert
from .openWeatherDay import OpenWeatherDay
from .openWeatherMoment import OpenWeatherMoment


@dataclass(frozen = True)
class OpenWeatherReport:
    latitude: float
    longitude: float
    alerts: list[OpenWeatherAlert]
    days: list[OpenWeatherDay]
    current: OpenWeatherMoment
    timeZone: tzinfo
