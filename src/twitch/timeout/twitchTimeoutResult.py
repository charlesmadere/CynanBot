from enum import Enum, auto


class TwitchTimeoutResult(Enum):

    ALREADY_BANNED_OR_TIMED_OUT = auto()
    API_CALL_FAILED = auto()
    FOLLOW_SHIELD = auto()
    IMMUNE_USER = auto()
    INVALID_USER_NAME = auto()
    IS_STREAMER = auto()
    SUCCESS = auto()
