from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchCheer:
    bits: int
