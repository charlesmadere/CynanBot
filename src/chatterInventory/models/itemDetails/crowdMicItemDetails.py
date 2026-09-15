from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class CrowdMicItemDetails:
    durationSeconds: int
