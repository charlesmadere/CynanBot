from dataclasses import dataclass


@dataclass(frozen = True)
class TimeoutBoosterPack:
    durationSeconds: int
    rewardId: str
