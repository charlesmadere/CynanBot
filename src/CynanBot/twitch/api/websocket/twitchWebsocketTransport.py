from dataclasses import dataclass
from datetime import datetime
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod


@dataclass(frozen = True)
class TwitchWebsocketTransport():
    connectedAt: datetime | None = None
    disconnectedAt: datetime | None = None
    secret: str | None = None
    sessionId: str | None = None
    method: TwitchWebsocketTransportMethod = TwitchWebsocketTransportMethod.WEBSOCKET

    def requireSessionId(self) -> str:
        if not utils.isValidStr(self.sessionId):
            raise ValueError(f'sessionId has not been set: \"{self}\"')

        return self.sessionId
