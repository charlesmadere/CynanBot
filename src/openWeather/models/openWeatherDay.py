from dataclasses import dataclass
from datetime import datetime

from frozenlist import FrozenList

from .openWeatherFeelsLike import OpenWeatherFeelsLike
from .openWeatherMomentDescription import OpenWeatherMomentDescription
from .openWeatherTemperature import OpenWeatherTemperature


@dataclass(frozen = True, slots = True)
class OpenWeatherDay:
    dateTime: datetime
    moonrise: datetime
    moonset: datetime
    sunrise: datetime
    sunset: datetime
    dewPoint: float
    moonPhase: float
    uvIndex: float
    windSpeed: float
    descriptions: FrozenList[OpenWeatherMomentDescription] | None
    humidity: int
    pressure: int
    feelsLike: OpenWeatherFeelsLike
    temperature: OpenWeatherTemperature
    summary: str
