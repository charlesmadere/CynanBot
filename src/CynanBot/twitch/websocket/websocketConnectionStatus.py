from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class WebsocketConnectionStatus(Enum):

    CONNECTED = auto()
    ENABLED = auto()
    RECONNECTING = auto()
    REVOKED = auto()
    USER_REMOVED = auto()
    VERSION_REMOVED = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'connected':
            return WebsocketConnectionStatus.CONNECTED
        elif text == 'enabled':
            return WebsocketConnectionStatus.ENABLED
        elif text == 'reconnecting':
            return WebsocketConnectionStatus.RECONNECTING
        elif text == 'authorization_revoked':
            return WebsocketConnectionStatus.REVOKED
        elif text == 'user_removed':
            return WebsocketConnectionStatus.USER_REMOVED
        elif text == 'version_removed':
            return WebsocketConnectionStatus.VERSION_REMOVED
        else:
            return None
