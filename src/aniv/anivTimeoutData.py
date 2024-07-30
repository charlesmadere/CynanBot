from dataclasses import dataclass


@dataclass(frozen = True)
class AnivTimeoutData:
    durationSeconds: int
    randomNumber: float
    timeoutProbability: float
