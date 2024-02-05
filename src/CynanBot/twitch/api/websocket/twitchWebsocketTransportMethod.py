from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class TwitchWebsocketTransportMethod(Enum):

    WEBHOOK = auto()
    WEBSOCKET = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'webhook':
            return TwitchWebsocketTransportMethod.WEBHOOK
        elif text == 'websocket':
            return TwitchWebsocketTransportMethod.WEBSOCKET
        else:
            raise ValueError(f'unknown WebsocketTransportMethod: \"{text}\"')

    def toStr(self) -> str:
        if self is TwitchWebsocketTransportMethod.WEBHOOK:
            return 'webhook'
        elif self is TwitchWebsocketTransportMethod.WEBSOCKET:
            return 'websocket'
        else:
            raise RuntimeError(f'unknown WebsocketTransportMethod: \"{self}\"')
