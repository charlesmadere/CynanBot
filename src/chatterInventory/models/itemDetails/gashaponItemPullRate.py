from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GashaponItemPullRate:
    pullRate: float
    iterations: int
    maximumPullAmount: int
    minimumPullAmount: int
