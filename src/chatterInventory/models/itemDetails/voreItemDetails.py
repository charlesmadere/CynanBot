from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class VoreItemDetails:
    inventoryMax: int | None
    timeoutDurationSeconds: int
