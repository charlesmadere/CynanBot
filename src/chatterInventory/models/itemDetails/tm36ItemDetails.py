from dataclasses import dataclass


@dataclass(frozen = True)
class Tm36ItemDetails:
    maxDurationSeconds: int
    minDurationSeconds: int
