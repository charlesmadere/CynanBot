from dataclasses import dataclass
from datetime import datetime

from CynanBot.openWeather.openWeatherAirPollutionIndex import \
    OpenWeatherAirPollutionIndex


@dataclass(frozen = True)
class OpenWeatherAirPollutionReport():
    dateTime: datetime
    latitude: float
    longitude: float
    airPollutionIndex: OpenWeatherAirPollutionIndex
