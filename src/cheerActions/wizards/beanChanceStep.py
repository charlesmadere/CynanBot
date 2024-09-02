from enum import auto

from .absStep import AbsStep


class BeanChanceStep(AbsStep):

    BITS = auto()
    MAXIMUM_PER_DAY = auto()
    RANDOM_CHANCE = auto()
