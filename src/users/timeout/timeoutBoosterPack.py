from dataclasses import dataclass

from .timeoutBoosterPackType import TimeoutBoosterPackType


@dataclass(frozen = True, slots = True)
class TimeoutBoosterPack:
    randomChanceEnabled: bool
    durationSeconds: int
    rewardId: str
    timeoutType: TimeoutBoosterPackType
