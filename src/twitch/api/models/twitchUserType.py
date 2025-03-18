from enum import Enum, auto


class TwitchUserType(Enum):

    ADMIN = auto()
    GLOBAL_MOD = auto()
    NORMAL = auto()
    STAFF = auto()
