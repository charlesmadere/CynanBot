from dataclasses import dataclass


@dataclass(frozen = True)
class RedemptionCounterBoosterPack:
    incrementAmount: int
    counterName: str
    emote: str | None
    rewardId: str
