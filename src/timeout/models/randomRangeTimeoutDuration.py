from dataclasses import dataclass

from .absTimeoutDuration import AbsTimeoutDuration


@dataclass(frozen = True)
class RandomRangeTimeoutDuration(AbsTimeoutDuration):
    maximumSeconds: int
    minimumSeconds: int
