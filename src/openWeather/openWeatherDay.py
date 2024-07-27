from dataclasses import dataclass
from datetime import datetime

from .openWeatherFeelsLike import OpenWeatherFeelsLike
from .openWeatherMomentDescription import OpenWeatherMomentDescription
from .openWeatherTemperature import OpenWeatherTemperature


@dataclass(frozen = True)
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
    humidity: int
    pressure: int
    descriptions: list[OpenWeatherMomentDescription] | None
    feelsLike: OpenWeatherFeelsLike
    temperature: OpenWeatherTemperature
    summary: str
