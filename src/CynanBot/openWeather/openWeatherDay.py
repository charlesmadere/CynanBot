from dataclasses import dataclass
from datetime import datetime

from CynanBot.openWeather.openWeatherFeelsLike import OpenWeatherFeelsLike
from CynanBot.openWeather.openWeatherMomentDescription import \
    OpenWeatherMomentDescription
from CynanBot.openWeather.openWeatherTemperature import OpenWeatherTemperature


@dataclass(frozen = True)
class OpenWeatherDay():
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
    feelsLike: OpenWeatherFeelsLike
    description: OpenWeatherMomentDescription
    temperature: OpenWeatherTemperature
    summary: str
