from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchCheerMetadata:
    bits: int
