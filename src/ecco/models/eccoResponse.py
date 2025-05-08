from dataclasses import dataclass


@dataclass(frozen = True)
class EccoResponse:
    hours: int
    minutes: int
    seconds: int
    rawText: str
