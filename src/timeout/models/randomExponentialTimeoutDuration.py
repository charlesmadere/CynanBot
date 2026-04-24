from dataclasses import dataclass

from .absTimeoutDuration import AbsTimeoutDuration


@dataclass(frozen = True, slots = True)
class RandomExponentialTimeoutDuration(AbsTimeoutDuration):
    exponent: int
    maximumSeconds: int
    minimumSeconds: int
