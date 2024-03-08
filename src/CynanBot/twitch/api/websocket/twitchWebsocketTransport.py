from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.misc.type_check import type_check
from CynanBot.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod


class TwitchWebsocketTransport():

    @type_check
    def __init__(
        self,
        connectedAt: SimpleDateTime | None = None,
        disconnectedAt: SimpleDateTime | None = None,
        secret: str | None = None,
        sessionId: str | None = None,
        method: TwitchWebsocketTransportMethod = TwitchWebsocketTransportMethod.WEBSOCKET,
    ):
        self.__connectedAt: SimpleDateTime | None = connectedAt
        self.__disconnectedAt: SimpleDateTime | None = disconnectedAt
        self.__secret: str | None = secret
        self.__sessionId: str | None = sessionId
        self.__method: TwitchWebsocketTransportMethod = method

    def getConnectedAt(self) -> SimpleDateTime | None:
        return self.__connectedAt

    def getDisconnectedAt(self) -> SimpleDateTime | None:
        return self.__disconnectedAt

    def getMethod(self) -> TwitchWebsocketTransportMethod:
        return self.__method

    def getSecret(self) -> str | None:
        return self.__secret

    def getSessionId(self) -> str | None:
        return self.__sessionId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireSessionId(self) -> str:
        sessionId = self.__sessionId

        if not utils.isValidStr(sessionId):
            raise ValueError(f'sessionId has not been set: \"{sessionId}\"')

        return sessionId

    def toDictionary(self) -> dict[str, Any]:
        return {
            'connectedAt': self.__connectedAt,
            'disconnectedAt': self.__disconnectedAt,
            'method': self.__method,
            'secret': self.__secret,
            'sessionId': self.__sessionId
        }
