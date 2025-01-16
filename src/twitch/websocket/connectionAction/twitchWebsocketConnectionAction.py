from enum import Enum, auto


class TwitchWebsocketConnectionAction(Enum):

    CREATE_EVENT_SUB_SUBSCRIPTION = auto()
    DISCONNECT = auto()
    OK = auto()
    RECONNECT = auto()
