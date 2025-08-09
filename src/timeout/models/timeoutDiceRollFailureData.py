from dataclasses import dataclass


@dataclass(frozen = True)
class TimeoutDiceRollFailureData:
    baseFailureProbability: float
    failureProbability: float
    maxBullyFailureProbability: float
    perBullyFailureProbabilityIncrease: float
    reverseProbability: float
    bullyOccurrences: int
    failureRoll: int
    maxBullyFailureOccurrences: int
    reverseRoll: int
