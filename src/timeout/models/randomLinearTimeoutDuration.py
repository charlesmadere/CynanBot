from dataclasses import dataclass

from .absTimeoutDuration import AbsTimeoutDuration


@dataclass(frozen = True)
class RandomLinearTimeoutDuration(AbsTimeoutDuration):
    maximumSeconds: int
    minimumSeconds: int
