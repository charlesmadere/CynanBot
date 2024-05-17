from enum import Enum, auto

import CynanBot.misc.utils as utils


class TwitchWebsocketTransportMethod(Enum):

    WEBHOOK = auto()
    WEBSOCKET = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        match text:
            case 'webhook': return TwitchWebsocketTransportMethod.WEBHOOK
            case 'websocket': return TwitchWebsocketTransportMethod.WEBSOCKET
            case _: raise ValueError(f'unknown WebsocketTransportMethod: \"{text}\"')

    def toStr(self) -> str:
        match self:
            case TwitchWebsocketTransportMethod.WEBHOOK: return 'webhook'
            case TwitchWebsocketTransportMethod.WEBSOCKET: return 'websocket'
            case _: raise RuntimeError(f'unknown WebsocketTransportMethod: \"{self}\"')
