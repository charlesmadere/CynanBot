from enum import Enum, auto


class TwitchWebsocketTransportMethod(Enum):

    WEBHOOK = auto()
    WEBSOCKET = auto()

    def toStr(self) -> str:
        match self:
            case TwitchWebsocketTransportMethod.WEBHOOK: return 'webhook'
            case TwitchWebsocketTransportMethod.WEBSOCKET: return 'websocket'
            case _: raise RuntimeError(f'unknown WebsocketTransportMethod: \"{self}\"')
