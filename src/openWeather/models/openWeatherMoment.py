from dataclasses import dataclass
from datetime import datetime

from frozenlist import FrozenList

from .openWeatherMomentDescription import OpenWeatherMomentDescription


@dataclass(frozen = True, slots = True)
class OpenWeatherMoment:
    dateTime: datetime
    sunrise: datetime
    sunset: datetime
    dewPoint: float
    feelsLikeTemperature: float
    temperature: float
    uvIndex: float
    windSpeed: float
    descriptions: FrozenList[OpenWeatherMomentDescription] | None
    humidity: int
    pressure: int
