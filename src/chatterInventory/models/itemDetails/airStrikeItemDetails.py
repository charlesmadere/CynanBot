from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AirStrikeItemDetails:
    maxDurationSeconds: int
    minDurationSeconds: int
    maxTargets: int
    minTargets: int
