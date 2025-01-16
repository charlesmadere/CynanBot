from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ....misc import utils as utils


@dataclass(frozen = True)
class TwitchWebsocketTransport:
    connectedAt: datetime | None
    disconnectedAt: datetime | None
    conduitId: str | None
    secret: str | None
    sessionId: str | None
    method: TwitchWebsocketTransportMethod

    def requireSessionId(self) -> str:
        if not utils.isValidStr(self.sessionId):
            raise ValueError(f'sessionId has not been set: \"{self}\"')

        return self.sessionId
