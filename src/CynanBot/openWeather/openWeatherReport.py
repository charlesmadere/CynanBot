from dataclasses import dataclass
from datetime import tzinfo

from CynanBot.openWeather.openWeatherMomentReport import \
    OpenWeatherMomentReport


@dataclass(frozen = True)
class OpenWeatherReport():
    latitude: float
    longitude: float
    current: OpenWeatherMomentReport
    timeZone: tzinfo
