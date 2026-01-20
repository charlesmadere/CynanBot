from dataclasses import dataclass

from .twitchWebsocketMetadata import TwitchWebsocketMetadata
from .twitchWebsocketPayload import TwitchWebsocketPayload


@dataclass(frozen = True, slots = True)
class TwitchWebsocketDataBundle:
    metadata: TwitchWebsocketMetadata
    payload: TwitchWebsocketPayload | None = None

    def requirePayload(self) -> TwitchWebsocketPayload:
        if self.payload is None:
            raise RuntimeError(f'this TwitchWebsocketDataBundle has no payload ({self})')

        return self.payload
