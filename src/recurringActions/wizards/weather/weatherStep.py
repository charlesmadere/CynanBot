from enum import auto

from ..absStep import AbsStep


class WeatherStep(AbsStep):

    ALERTS_ONLY = auto()
    MINUTES_BETWEEN = auto()
