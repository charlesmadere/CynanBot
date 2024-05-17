from dataclasses import dataclass

from CynanBot.twitch.api.websocket.twitchWebsocketMetadata import \
    TwitchWebsocketMetadata
from CynanBot.twitch.api.websocket.twitchWebsocketPayload import \
    TwitchWebsocketPayload


@dataclass(frozen = True)
class TwitchWebsocketDataBundle():
    metadata: TwitchWebsocketMetadata
    payload: TwitchWebsocketPayload | None = None

    def requirePayload(self) -> TwitchWebsocketPayload:
        if self.payload is None:
            raise RuntimeError(f'this TwitchWebsocketDataBundle has no payload ({self})')

        return self.payload
