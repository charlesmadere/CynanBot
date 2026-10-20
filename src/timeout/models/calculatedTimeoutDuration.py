from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class CalculatedTimeoutDuration:
    seconds: int
    message: str
    shorthandMessage: str
