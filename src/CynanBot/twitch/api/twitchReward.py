from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchReward():
    cost: int
    prompt: str | None
    rewardId: str
    title: str
