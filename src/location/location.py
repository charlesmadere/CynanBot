from dataclasses import dataclass
from datetime import tzinfo


@dataclass(frozen = True, slots = True)
class Location:
    latitude: float
    longitude: float
    locationId: str
    name: str
    timeZone: tzinfo
