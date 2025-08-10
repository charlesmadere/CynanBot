from enum import Enum, auto


class TimeoutStreamStatusRequirement(Enum):

    ANY = auto()
    OFFLINE = auto()
    ONLINE = auto()
