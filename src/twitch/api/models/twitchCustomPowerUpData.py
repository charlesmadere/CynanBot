from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchCustomPowerUpData:
    rewardId: str
    title: str
