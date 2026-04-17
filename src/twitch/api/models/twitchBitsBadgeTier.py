from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchBitsBadgeTier:
    tier: int
