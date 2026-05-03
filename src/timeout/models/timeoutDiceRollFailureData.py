from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TimeoutDiceRollFailureData:
    failureProbability: float
    reverseProbability: float
    failureRoll: int
    reverseRoll: int
