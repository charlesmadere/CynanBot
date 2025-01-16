from enum import auto

from ..absStep import AbsStep


class TntTimeoutStep(AbsStep):

    BITS = auto()
    DURATION_SECONDS = auto()
    MAXIMUM_CHATTERS = auto()
    MINIMUM_CHATTERS = auto()
