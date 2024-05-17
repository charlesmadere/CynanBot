from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchWebsocketMessageType(Enum):

    KEEP_ALIVE = auto()
    NOTIFICATION = auto()
    RECONNECT = auto()
    REVOCATION = auto()
    WELCOME = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        match text:
            case 'session_keepalive': return TwitchWebsocketMessageType.KEEP_ALIVE
            case 'notification': return TwitchWebsocketMessageType.NOTIFICATION
            case 'session_reconnect': return TwitchWebsocketMessageType.RECONNECT
            case 'revocation': return TwitchWebsocketMessageType.REVOCATION
            case 'session_welcome': return TwitchWebsocketMessageType.WELCOME
            case _: return None
