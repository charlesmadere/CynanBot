from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class WebsocketMessageType(Enum):

    KEEP_ALIVE = auto()
    NOTIFICATION = auto()
    RECONNECT = auto()
    REVOCATION = auto()
    WELCOME = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'session_keepalive':
            return WebsocketMessageType.KEEP_ALIVE
        elif text == 'notification':
            return WebsocketMessageType.NOTIFICATION
        elif text == 'session_reconnect':
            return WebsocketMessageType.RECONNECT
        elif text == 'revocation':
            return WebsocketMessageType.REVOCATION
        elif text == 'session_welcome':
            return WebsocketMessageType.WELCOME
        else:
            return None
