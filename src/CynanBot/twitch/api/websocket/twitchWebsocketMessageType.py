from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchWebsocketMessageType(Enum):

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
            return TwitchWebsocketMessageType.KEEP_ALIVE
        elif text == 'notification':
            return TwitchWebsocketMessageType.NOTIFICATION
        elif text == 'session_reconnect':
            return TwitchWebsocketMessageType.RECONNECT
        elif text == 'revocation':
            return TwitchWebsocketMessageType.REVOCATION
        elif text == 'session_welcome':
            return TwitchWebsocketMessageType.WELCOME
        else:
            return None
