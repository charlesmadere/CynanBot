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

        match text:
            case 'connected': return TwitchWebsocketConnectionStatus.CONNECTED
            case 'enabled': return TwitchWebsocketConnectionStatus.ENABLED
            case 'reconnecting': return TwitchWebsocketConnectionStatus.RECONNECTING
            case 'authorization_revoked': return TwitchWebsocketConnectionStatus.REVOKED
            case 'user_removed': return TwitchWebsocketConnectionStatus.USER_REMOVED
            case 'version_removed': return TwitchWebsocketConnectionStatus.VERSION_REMOVED
            case _: return None
