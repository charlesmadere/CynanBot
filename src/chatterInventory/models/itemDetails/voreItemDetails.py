from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class VoreItemDetails:
    timeoutDurationSeconds: int
