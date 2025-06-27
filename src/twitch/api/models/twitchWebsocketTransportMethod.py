from enum import Enum, auto


class TwitchWebsocketTransportMethod(Enum):

    CONDUIT = auto()
    WEBHOOK = auto()
    WEBSOCKET = auto()
