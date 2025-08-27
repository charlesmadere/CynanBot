from dataclasses import dataclass


@dataclass(frozen = True)
class AirStrikeItemDetails:
    maxDurationSeconds: int
    minDurationSeconds: int
    maxTargets: int
    minTargets: int
