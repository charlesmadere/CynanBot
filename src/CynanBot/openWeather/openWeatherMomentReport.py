from dataclasses import dataclass


@dataclass(frozen = True)
class OpenWeatherMomentReport():
    feelsLikeTemperature: float
    temperature: float
    uvIndex: float
    windSpeed: float
    humidity: int
    pressure: int
    sunrise: int
    sunset: int
