from enum import auto

from .absStep import AbsStep


class TimeoutStep(AbsStep):

    BITS = auto()
    DURATION_SECONDS = auto()
    STREAM_STATUS = auto()
