from dataclasses import dataclass
from datetime import datetime, tzinfo

from .openWeatherAirPollutionIndex import OpenWeatherAirPollutionIndex


@dataclass(frozen = True, slots = True)
class OpenWeatherAirPollutionReport:
    dateTime: datetime
    latitude: float
    longitude: float
    airPollutionIndex: OpenWeatherAirPollutionIndex
    timeZone: tzinfo
