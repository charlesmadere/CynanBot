from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GrenadeItemDetails:
    inventoryMax: int | None
    maxDurationSeconds: int
    minDurationSeconds: int
