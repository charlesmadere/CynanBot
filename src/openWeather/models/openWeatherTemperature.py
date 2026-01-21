from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class OpenWeatherTemperature:
    day: float
    evening: float
    maximum: float
    minimum: float
    morning: float
    night: float
