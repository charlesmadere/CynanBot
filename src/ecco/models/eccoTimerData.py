from dataclasses import dataclass


@dataclass(frozen = True)
class EccoTimerData:
    hours: int
    minutes: int
    seconds: int
    rawText: str
