from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class OpenWeatherMomentDescription:
    description: str
    descriptionId: str
    emoji: str | None
    icon: str
    main: str
