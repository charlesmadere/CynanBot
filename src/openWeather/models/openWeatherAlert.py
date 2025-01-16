from dataclasses import dataclass


@dataclass(frozen = True)
class OpenWeatherAlert:
    end: int
    start: int
    description: str
    event: str
    senderName: str
