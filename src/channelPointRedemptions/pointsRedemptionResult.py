from enum import Enum, auto


class PointsRedemptionResult(Enum):

    CONSUMED = auto()
    HANDLED = auto()
    IGNORED = auto()
