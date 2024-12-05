from dataclasses import dataclass


@dataclass(frozen = True)
class TimeoutBoosterPack:
    randomChanceEnabled: bool
    durationSeconds: int
    rewardId: str
