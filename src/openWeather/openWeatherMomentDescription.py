from dataclasses import dataclass


@dataclass(frozen = True)
class OpenWeatherMomentDescription():
    description: str
    descriptionId: str
    emoji: str | None
    icon: str
    main: str
