from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class OpenWeatherMomentReport():
    dateTime: datetime
    feelsLikeTemperature: float
    temperature: float
    uvIndex: float
    windSpeed: float
    humidity: int
    pressure: int
    sunrise: int
    sunset: int
