from enum import auto

from CynanBot.cheerActions.wizards.absStep import AbsStep


class TimeoutStep(AbsStep):

    BITS = auto()
    DURATION_SECONDS = auto()
    STREAM_STATUS = auto()
