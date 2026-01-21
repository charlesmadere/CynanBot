from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GrenadeItemDetails:
    maxDurationSeconds: int
    minDurationSeconds: int
