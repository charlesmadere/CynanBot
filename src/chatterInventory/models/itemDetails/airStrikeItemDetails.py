from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AirStrikeItemDetails:
    inventoryMax: int | None
    maxDurationSeconds: int
    minDurationSeconds: int
    maxTargets: int
    minTargets: int
