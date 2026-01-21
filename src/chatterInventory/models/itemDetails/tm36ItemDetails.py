from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class Tm36ItemDetails:
    maxDurationSeconds: int
    minDurationSeconds: int
