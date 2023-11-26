from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class WebsocketTransportMethod(Enum):

    WEBHOOK = auto()
    WEBSOCKET = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'webhook':
            return WebsocketTransportMethod.WEBHOOK
        elif text == 'websocket':
            return WebsocketTransportMethod.WEBSOCKET
        else:
            raise ValueError(f'unknown WebsocketTransportMethod: \"{text}\"')

    def toStr(self) -> str:
        if self is WebsocketTransportMethod.WEBHOOK:
            return 'webhook'
        elif self is WebsocketTransportMethod.WEBSOCKET:
            return 'websocket'
        else:
            raise RuntimeError(f'unknown WebsocketTransportMethod: \"{self}\"')
