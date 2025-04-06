from enum import auto

from ..absStep import AbsStep


class TimeoutStep(AbsStep):

    BITS = auto()
    DURATION_SECONDS = auto()
    RANDOM_CHANCE_ENABLED = auto()
    STREAM_STATUS = auto()
    TARGET_TYPE = auto()
