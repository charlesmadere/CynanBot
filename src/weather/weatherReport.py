from dataclasses import dataclass

from ..location.location import Location
from ..openWeather.openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from ..openWeather.openWeatherReport import OpenWeatherReport


@dataclass(frozen = True)
class WeatherReport:
    location: Location
    airPollution: OpenWeatherAirPollutionReport | None
    report: OpenWeatherReport
