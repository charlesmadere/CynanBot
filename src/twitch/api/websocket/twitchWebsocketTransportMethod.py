from enum import Enum, auto


class TwitchWebsocketTransportMethod(Enum):

    CONDUIT = auto()
    WEBHOOK = auto()
    WEBSOCKET = auto()

    def toStr(self) -> str:
        match self:
            case TwitchWebsocketTransportMethod.CONDUIT: return 'conduit'
            case TwitchWebsocketTransportMethod.WEBHOOK: return 'webhook'
            case TwitchWebsocketTransportMethod.WEBSOCKET: return 'websocket'
            case _: raise RuntimeError(f'unknown WebsocketTransportMethod: \"{self}\"')
