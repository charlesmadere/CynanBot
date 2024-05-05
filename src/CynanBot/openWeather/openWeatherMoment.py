from dataclasses import dataclass
from datetime import datetime

from CynanBot.openWeather.openWeatherMomentDescription import \
    OpenWeatherMomentDescription


@dataclass(frozen = True)
class OpenWeatherMoment():
    dateTime: datetime
    dewPoint: float
    feelsLikeTemperature: float
    temperature: float
    uvIndex: float
    windSpeed: float
    humidity: int
    pressure: int
    sunrise: int
    sunset: int
    description: OpenWeatherMomentDescription
