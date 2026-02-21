from enum import Enum, auto


class WebsocketEventType(Enum):

    CHANNEL_PREDICTION = auto()
    MOUSE_CURSOR = auto()
