from enum import Enum, auto


class TwitchPollStatus(Enum):

    ACTIVE = auto()
    ARCHIVED = auto()
    COMPLETED = auto()
    INVALID = auto()
    TERMINATED = auto()
