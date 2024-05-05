from dataclasses import dataclass


@dataclass(frozen = True)
class OpenWeatherMomentDescription():
    description: str
    descriptionId: str
    icon: str
    main: str
