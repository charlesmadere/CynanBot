from dataclasses import dataclass


@dataclass(frozen = True)
class VoreItemDetails:
    timeoutDurationSeconds: int
