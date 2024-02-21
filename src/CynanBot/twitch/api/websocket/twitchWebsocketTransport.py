from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod


class TwitchWebsocketTransport():

    def __init__(
        self,
        connectedAt: Optional[SimpleDateTime] = None,
        disconnectedAt: Optional[SimpleDateTime] = None,
        secret: Optional[str] = None,
        sessionId: Optional[str] = None,
        method: TwitchWebsocketTransportMethod = TwitchWebsocketTransportMethod.WEBSOCKET,
    ):
        assert connectedAt is None or isinstance(connectedAt, SimpleDateTime), f"malformed {connectedAt=}"
        assert disconnectedAt is None or isinstance(disconnectedAt, SimpleDateTime), f"malformed {disconnectedAt=}"
        assert secret is None or isinstance(secret, str), f"malformed {secret=}"
        assert sessionId is None or isinstance(sessionId, str), f"malformed {sessionId=}"
        assert isinstance(method, TwitchWebsocketTransportMethod), f"malformed {method=}"

        self.__connectedAt: Optional[SimpleDateTime] = connectedAt
        self.__disconnectedAt: Optional[SimpleDateTime] = disconnectedAt
        self.__secret: Optional[str] = secret
        self.__sessionId: Optional[str] = sessionId
        self.__method: TwitchWebsocketTransportMethod = method

    def getConnectedAt(self) -> Optional[SimpleDateTime]:
        return self.__connectedAt

    def getDisconnectedAt(self) -> Optional[SimpleDateTime]:
        return self.__disconnectedAt

    def getMethod(self) -> TwitchWebsocketTransportMethod:
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
            'sessionId': self.__sessionId
        }
    