from dataclasses import dataclass

from ..location.location import Location
from ..openWeather.models.openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from ..openWeather.models.openWeatherReport import OpenWeatherReport


@dataclass(frozen = True)
class WeatherReport:
    location: Location
    airPollution: OpenWeatherAirPollutionReport | None
    report: OpenWeatherReport
