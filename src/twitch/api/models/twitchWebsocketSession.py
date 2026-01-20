from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus


@dataclass(frozen = True, slots = True)
class TwitchWebsocketSession:
    connectedAt: datetime
    keepAliveTimeoutSeconds: int | None
    reconnectUrl: str | None
    recoveryUrl: str | None
    sessionId: str
    status: TwitchWebsocketConnectionStatus
