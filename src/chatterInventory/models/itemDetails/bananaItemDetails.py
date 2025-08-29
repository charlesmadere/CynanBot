from dataclasses import dataclass


@dataclass(frozen = True)
class BananaItemDetails:
    randomChanceEnabled: bool
    durationSeconds: int
