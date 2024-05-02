from dataclasses import dataclass
from datetime import datetime

from CynanBot.openWeather.openWeatherAirQualityIndex import OpenWeatherAirQualityIndex


@dataclass(frozen = True)
class OpenWeatherAirQualityReport():
    dateTime: datetime
    latitude: float
    longitude: float
    airQualityIndex: OpenWeatherAirQualityIndex
