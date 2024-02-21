from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.api.websocket.twitchWebsocketMessageType import \
    TwitchWebsocketMessageType
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType


class TwitchWebsocketMetadata():

    def __init__(
        self,
        messageTimestamp: SimpleDateTime,
        messageId: str,
        subscriptionVersion: Optional[str],
        messageType: Optional[TwitchWebsocketMessageType],
        subscriptionType: Optional[TwitchWebsocketSubscriptionType]
    ):
        assert isinstance(messageTimestamp, SimpleDateTime), f"malformed {messageTimestamp=}"
        if not utils.isValidStr(messageId):
            raise TypeError(f'messageId argument is malformed: \"{messageId}\"')
        assert subscriptionVersion is None or isinstance(subscriptionVersion, str), f"malformed {subscriptionVersion=}"
        assert messageType is None or isinstance(messageType, TwitchWebsocketMessageType), f"malformed {messageType=}"
        assert subscriptionType is None or isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        self.__messageTimestamp: SimpleDateTime = messageTimestamp
        self.__messageId: str = messageId
        self.__subscriptionVersion: Optional[str] = subscriptionVersion
        self.__messageType: Optional[TwitchWebsocketMessageType] = messageType
        self.__subscriptionType: Optional[TwitchWebsocketSubscriptionType] = subscriptionType

    def getMessageId(self) -> str:
        return self.__messageId

    def getMessageTimestamp(self) -> SimpleDateTime:
        return self.__messageTimestamp

    def getMessageType(self) -> Optional[TwitchWebsocketMessageType]:
        return self.__messageType

    def getSubscriptionType(self) -> Optional[TwitchWebsocketSubscriptionType]:
        return self.__subscriptionType

    def getSubscriptionVersion(self) -> Optional[str]:
        return self.__subscriptionVersion

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'messageId': self.__messageId,
            'messageTimestamp': self.__messageTimestamp,
            'messageType': self.__messageType,
            'subscriptionType': self.__subscriptionType,
            'subscriptionVersion': self.__subscriptionVersion
        }
