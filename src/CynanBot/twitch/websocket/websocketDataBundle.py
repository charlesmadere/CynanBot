from typing import Any, Dict, Optional

from CynanBot.twitch.websocket.websocketMetadata import WebsocketMetadata
from CynanBot.twitch.websocket.websocketPayload import WebsocketPayload


class WebsocketDataBundle():

    def __init__(
        self,
        metadata: WebsocketMetadata,
        payload: Optional[WebsocketPayload] = None
    ):
        if not isinstance(metadata, WebsocketMetadata):
            raise ValueError(f'metadata argument is malformed: \"{metadata}\"')
        if payload is not None and not isinstance(payload, WebsocketPayload):
            raise ValueError(f'payload argument is malformed: \"{payload}\"')

        self.__metadata: WebsocketMetadata = metadata
        self.__payload: Optional[WebsocketPayload] = payload

    def getMetadata(self) -> WebsocketMetadata:
        return self.__metadata

    def getPayload(self) -> Optional[WebsocketPayload]:
        return self.__payload

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requirePayload(self) -> WebsocketPayload:
        payload = self.__payload

        if payload is None:
            raise RuntimeError(f'this WebsocketDataBundle has no payload (metadata=\"{self.__metadata}\")')

        return payload

    def toDictionary(self) -> Dict[str, Any]:
        dictionary: Dict[str, Any] = {
            'metadata': self.__metadata.toDictionary()
        }

        if self.__payload is None:
            dictionary['payload'] = None
        else:
            dictionary['payload'] = self.__payload.toDictionary()

        return dictionary
