from dataclasses import dataclass

from .timeoutBoosterPackType import TimeoutBoosterPackType


@dataclass(frozen = True)
class TimeoutBoosterPack:
    randomChanceEnabled: bool
    durationSeconds: int
    rewardId: str
    timeoutType: TimeoutBoosterPackType
