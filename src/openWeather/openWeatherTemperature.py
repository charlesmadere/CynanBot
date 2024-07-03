from dataclasses import dataclass


@dataclass(frozen = True)
class OpenWeatherTemperature():
    day: float
    evening: float
    maximum: float
    minimum: float
    morning: float
    night: float
