from dataclasses import dataclass


@dataclass(frozen = True)
class TimeoutRollFailureData:
    baseFailureProbability: float
    failureProbability: float
    maxBullyFailureProbability: float
    perBullyFailureProbabilityIncrease: float
    reverseProbability: float
    bullyOccurrences: int
    failureRoll: int
    maxBullyFailureOccurrences: int
    reverseRoll: int
