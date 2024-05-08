from dataclasses import dataclass

from CynanBot.location.location import Location
from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport


@dataclass(frozen = True)
class WeatherReport():
    location: Location
    airPollution: OpenWeatherAirPollutionReport | None
    report: OpenWeatherReport
