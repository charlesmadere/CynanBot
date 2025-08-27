from dataclasses import dataclass


@dataclass(frozen = True)
class GrenadeItemDetails:
    maxDurationSeconds: int
    minDurationSeconds: int
