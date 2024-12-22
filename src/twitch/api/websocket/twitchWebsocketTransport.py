from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ....misc import utils as utils


@dataclass(frozen = True)
class TwitchWebsocketTransport:
    connectedAt: datetime | None = None
    disconnectedAt: datetime | None = None
    conduitId: str | None = None
    secret: str | None = None
    sessionId: str | None = None
    method: TwitchWebsocketTransportMethod = TwitchWebsocketTransportMethod.WEBSOCKET

    def requireSessionId(self) -> str:
        if not utils.isValidStr(self.sessionId):
            raise ValueError(f'sessionId has not been set: \"{self}\"')

        return self.sessionId
