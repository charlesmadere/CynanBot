from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class Tm36ItemDetails:
    dudSpecialEffectEnabled: bool
    inventoryMax: int | None
    maxDurationSeconds: int
    minDurationSeconds: int
