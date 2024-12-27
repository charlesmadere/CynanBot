from enum import auto

from ..absStep import AbsStep


class TimeoutStep(AbsStep):

    BITS = auto()
    DURATION_SECONDS = auto()
    RANDOM_CHANCE_ENABLED = auto()
    STREAM_STATUS = auto()
    TARGETS_RANDOM_ACTIVE_CHATTER = auto()
