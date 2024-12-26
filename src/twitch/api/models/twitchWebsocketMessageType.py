from enum import Enum, auto


class TwitchWebsocketMessageType(Enum):

    KEEP_ALIVE = auto()
    NOTIFICATION = auto()
    RECONNECT = auto()
    REVOCATION = auto()
    WELCOME = auto()
