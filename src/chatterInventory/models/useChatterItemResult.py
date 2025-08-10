from enum import Enum, auto


class UseChatterItemResult(Enum):

    FEATURE_DISABLED = auto()
    INVALID_REQUEST = auto()
    ITEM_DISABLED = auto()
    OK = auto()
