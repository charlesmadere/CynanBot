from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchCustomPowerUpData:
    bits: int | None
    prompt: str | None
    rewardId: str
    title: str
