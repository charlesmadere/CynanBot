from dataclasses import dataclass


@dataclass(frozen = True)
class CalculatedTimeoutDuration:
    seconds: int
    message: str
