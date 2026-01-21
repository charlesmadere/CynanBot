from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class OpenWeatherFeelsLike:
    day: float
    evening: float
    morning: float
    night: float
