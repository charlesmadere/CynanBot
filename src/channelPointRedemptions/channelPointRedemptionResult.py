from enum import Enum, auto


class ChannelPointRedemptionResult(Enum):

    CONSUMED = auto()
    HANDLED = auto()
    IGNORED = auto()
