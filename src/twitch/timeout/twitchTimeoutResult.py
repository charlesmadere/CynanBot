from enum import Enum, auto


class TwitchTimeoutResult(Enum):

    ALREADY_TIMED_OUT = auto()
    API_CALL_FAILED = auto()
    BANNED = auto()
    CANT_UNMOD = auto()
    IMMUNE_USER = auto()
    INVALID_USER_NAME = auto()
    IS_STREAMER = auto()
    SUCCESS = auto()
