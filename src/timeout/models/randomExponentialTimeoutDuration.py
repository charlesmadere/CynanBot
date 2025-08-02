from dataclasses import dataclass

from .absTimeoutDuration import AbsTimeoutDuration


@dataclass(frozen = True)
class RandomExponentialTimeoutDuration(AbsTimeoutDuration):
    scale: float
    maximumSeconds: int
    minimumSeconds: int
