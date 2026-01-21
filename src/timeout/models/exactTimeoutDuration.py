from dataclasses import dataclass

from .absTimeoutDuration import AbsTimeoutDuration


@dataclass(frozen = True, slots = True)
class ExactTimeoutDuration(AbsTimeoutDuration):
    seconds: int
