from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchCustomPowerUp:
    bits: int
    powerUpId: str
    prompt: str | None
    title: str
