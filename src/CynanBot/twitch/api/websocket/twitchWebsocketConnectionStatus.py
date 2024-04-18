from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchWebsocketConnectionStatus(Enum):

    CONNECTED = auto()
    ENABLED = auto()
    RECONNECTING = auto()
    REVOKED = auto()
    USER_REMOVED = auto()
    VERSION_REMOVED = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'connected':
            return TwitchWebsocketConnectionStatus.CONNECTED
        elif text == 'enabled':
            return TwitchWebsocketConnectionStatus.ENABLED
        elif text == 'reconnecting':
            return TwitchWebsocketConnectionStatus.RECONNECTING
        elif text == 'authorization_revoked':
            return TwitchWebsocketConnectionStatus.REVOKED
        elif text == 'user_removed':
            return TwitchWebsocketConnectionStatus.USER_REMOVED
        elif text == 'version_removed':
            return TwitchWebsocketConnectionStatus.VERSION_REMOVED
        else:
            return None
