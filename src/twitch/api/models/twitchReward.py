from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchReward:
    cost: int
    prompt: str | None
    rewardId: str
    title: str
