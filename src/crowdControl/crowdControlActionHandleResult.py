from enum import Enum, auto


class CrowdControlActionHandleResult(Enum):

    ABANDON = auto()
    OK = auto()
    RETRY = auto()
