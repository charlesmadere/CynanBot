from dataclasses import dataclass
from datetime import tzinfo

from frozenlist import FrozenList

from .openWeatherAlert import OpenWeatherAlert
from .openWeatherDay import OpenWeatherDay
from .openWeatherMoment import OpenWeatherMoment


@dataclass(frozen = True, slots = True)
class OpenWeatherReport:
    latitude: float
    longitude: float
    alerts: FrozenList[OpenWeatherAlert]
    days: FrozenList[OpenWeatherDay]
    current: OpenWeatherMoment
    timeZone: tzinfo
