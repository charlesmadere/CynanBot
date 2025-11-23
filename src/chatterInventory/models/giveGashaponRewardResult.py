from enum import Enum, auto


class GiveGashaponRewardResult(Enum):

    FEATURE_DISABLED = auto()
    NOT_READY = auto()
    NOT_SUBSCRIBED = auto()
    REWARDED = auto()
