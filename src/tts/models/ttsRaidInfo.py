from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TtsRaidInfo:
    viewers: int
