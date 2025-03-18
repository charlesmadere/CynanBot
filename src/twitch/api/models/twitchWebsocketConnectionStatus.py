from enum import Enum, auto


class TwitchWebsocketConnectionStatus(Enum):

    CONNECTED = auto()
    ENABLED = auto()
    RECONNECTING = auto()
    REVOKED = auto()
    USER_REMOVED = auto()
    VERSION_REMOVED = auto()
    WEBHOOK_CALLBACK_VERIFICATION_PENDING = auto()
