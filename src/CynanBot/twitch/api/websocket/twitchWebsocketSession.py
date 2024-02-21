from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus


class TwitchWebsocketSession():

    def __init__(
        self,
        keepAliveTimeoutSeconds: int,
        connectedAt: SimpleDateTime,
        reconnectUrl: Optional[str],
        sessionId: str,
        status: Optional[TwitchWebsocketConnectionStatus]
    ):
        if not utils.isValidInt(keepAliveTimeoutSeconds):
            raise ValueError(f'keepAliveTimeoutSeconds argument is malformed: \"{keepAliveTimeoutSeconds}\"')
        assert isinstance(connectedAt, SimpleDateTime), f"malformed {connectedAt=}"
        if reconnectUrl is not None and not utils.isValidUrl(reconnectUrl):
            raise ValueError(f'reconnectUrl argument is malformed: \"{reconnectUrl}\"')
        if not utils.isValidStr(sessionId):
            raise ValueError(f'sessionId argument is malformed: \"{sessionId}\"')
        assert status is None or isinstance(status, TwitchWebsocketConnectionStatus), f"malformed {status=}"

        self.__keepAliveTimeoutSeconds: int = keepAliveTimeoutSeconds
        self.__connectedAt: SimpleDateTime = connectedAt
        self.__reconnectUrl: Optional[str] = reconnectUrl
        self.__sessionId: str = sessionId
        self.__status: Optional[TwitchWebsocketConnectionStatus] = status

    def getConnectedAt(self) -> SimpleDateTime:
        return self.__connectedAt

    def getKeepAliveTimeoutSeconds(self) -> int:
        return self.__keepAliveTimeoutSeconds

    def getReconnectUrl(self) -> Optional[str]:
        return self.__reconnectUrl

    def getSessionId(self) -> str:
        return self.__sessionId

    def getStatus(self) -> Optional[TwitchWebsocketConnectionStatus]:
        return self.__status

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'connectedAt': self.__connectedAt,
            'keepAliveTimeoutSeconds': self.__keepAliveTimeoutSeconds,
            'reconnectUrl': self.__reconnectUrl,
            'sessionId': self.__sessionId,
            'status': self.__status
        }
