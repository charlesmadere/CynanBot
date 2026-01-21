from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class BananaItemDetails:
    randomChanceEnabled: bool
    durationSeconds: int
