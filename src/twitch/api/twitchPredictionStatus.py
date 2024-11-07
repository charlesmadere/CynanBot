from enum import Enum, auto


class TwitchPredictionStatus(Enum):

    ACTIVE = auto()
    CANCELED = auto()
    LOCKED = auto()
    RESOLVED = auto()
