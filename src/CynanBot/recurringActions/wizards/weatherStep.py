from enum import auto

from CynanBot.recurringActions.wizards.absStep import AbsStep


class WeatherStep(AbsStep):

    ALERTS_ONLY = auto()
    MINUTES_BETWEEN = auto()
