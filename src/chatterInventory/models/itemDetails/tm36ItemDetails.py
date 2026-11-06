from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class Tm36ItemDetails:
    inventoryMax: int | None
    maxDurationSeconds: int
    minDurationSeconds: int
