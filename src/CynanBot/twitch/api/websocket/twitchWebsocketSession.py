from dataclasses import dataclass
from datetime import datetime

from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus


@dataclass(frozen = True)
class TwitchWebsocketSession():
    connectedAt: datetime
    keepAliveTimeoutSeconds: int
    reconnectUrl: str | None
    sessionId: str
    status: TwitchWebsocketConnectionStatus | None
