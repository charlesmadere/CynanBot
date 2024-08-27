from enum import Enum, auto


class CrowdControlInputResult(Enum):

    ABANDON = auto()
    OK = auto()
    RETRY = auto()
