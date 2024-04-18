from typing import Any

from CynanBot.twitch.api.websocket.twitchWebsocketMetadata import \
    TwitchWebsocketMetadata
from CynanBot.twitch.api.websocket.twitchWebsocketPayload import \
    TwitchWebsocketPayload


class TwitchWebsocketDataBundle():

    def __init__(
        self,
        metadata: TwitchWebsocketMetadata,
        payload: TwitchWebsocketPayload | None = None
    ):
        if not isinstance(metadata, TwitchWebsocketMetadata):
            raise TypeError(f'metadata argument is malformed: \"{metadata}\"')
        if payload is not None and not isinstance(payload, TwitchWebsocketPayload):
            raise TypeError(f'payload argument is malformed: \"{payload}\"')

        self.__metadata: TwitchWebsocketMetadata = metadata
        self.__payload: TwitchWebsocketPayload | None = payload

    def getMetadata(self) -> TwitchWebsocketMetadata:
        return self.__metadata

    def getPayload(self) -> TwitchWebsocketPayload | None:
        return self.__payload

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requirePayload(self) -> TwitchWebsocketPayload:
        payload = self.__payload

        if payload is None:
            raise RuntimeError(f'this WebsocketDataBundle has no payload ({self})')

        return payload

    def toDictionary(self) -> dict[str, Any]:
        return {
            'metadata': self.__metadata,
            'payload': self.__payload
        }
