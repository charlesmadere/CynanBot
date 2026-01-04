from enum import Enum, auto


class GiveGashaponRewardResult(Enum):

    CHATTER_INVENTORY_DISABLED = auto()
    GASHAPON_ITEM_DISABLED = auto()
    NOT_FOLLOWING = auto()
    NOT_READY = auto()
    NOT_SUBSCRIBED = auto()
    REWARDED = auto()
