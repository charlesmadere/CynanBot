from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.websocket.websocketTransportMethod import \
    WebsocketTransportMethod


class WebsocketTransport():

    def __init__(
        self,
        connectedAt: Optional[SimpleDateTime] = None,
        disconnectedAt: Optional[SimpleDateTime] = None,
        secret: Optional[str] = None,
        sessionId: Optional[str] = None,
        method: WebsocketTransportMethod = WebsocketTransportMethod.WEBSOCKET,
    ):
        if connectedAt is not None and not isinstance(connectedAt, SimpleDateTime):
            raise ValueError(f'connectedAt argument is malformed: \"{connectedAt}\"')
        elif disconnectedAt is not None and not isinstance(disconnectedAt, SimpleDateTime):
            raise ValueError(f'disconnectedAt argument is malformed: \"{disconnectedAt}\"')
        elif secret is not None and not isinstance(secret, str):
            raise ValueError(f'secret argument is malformed: \"{secret}\"')
        elif sessionId is not None and not isinstance(sessionId, str):
            raise ValueError(f'sessionId argument is malformed: \"{sessionId}\"')
        elif not isinstance(method, WebsocketTransportMethod):
            raise ValueError(f'method argument is malformed: \"{method}\"')

        self.__connectedAt: Optional[SimpleDateTime] = connectedAt
        self.__disconnectedAt: Optional[SimpleDateTime] = disconnectedAt
        self.__secret: Optional[str] = secret
        self.__sessionId: Optional[str] = sessionId
        self.__method: WebsocketTransportMethod = method

    def getConnectedAt(self) -> Optional[SimpleDateTime]:
        return self.__connectedAt

    def getDisconnectedAt(self) -> Optional[SimpleDateTime]:
        return self.__disconnectedAt

    def getMethod(self) -> WebsocketTransportMethod:
        return self.__method

    def getSecret(self) -> Optional[str]:
        return self.__secret

    def getSessionId(self) -> Optional[str]:
        return self.__sessionId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireSessionId(self) -> str:
        sessionId = self.__sessionId

        if not utils.isValidStr(sessionId):
            raise ValueError(f'sessionId has not been set: \"{sessionId}\"')

        return sessionId

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'connectedAt': self.__connectedAt,
            'disconnectedAt': self.__disconnectedAt,
            'method': self.__method,
            'secret': self.__secret,
            'sesssionId': self.__sessionId
        }
    