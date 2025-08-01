from dataclasses import dataclass

from .absTimeoutDuration import AbsTimeoutDuration


@dataclass(frozen = True)
class RandomExponentialTimeoutDuration(AbsTimeoutDuration):
    exponent: float
    maximumSeconds: int
    minimumSeconds: int
