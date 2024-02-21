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
        if not isinstance(messageTimestamp, SimpleDateTime):
            raise TypeError(f'messageTimestamp argument is malformed: \"{messageTimestamp}\"')
        elif not utils.isValidStr(messageId):
            raise TypeError(f'messageId argument is malformed: \"{messageId}\"')
        elif subscriptionVersion is not None and not isinstance(subscriptionVersion, str):
            raise TypeError(f'subscriptionVersion argument is malformed: \"{subscriptionVersion}\"')
        elif messageType is not None and not isinstance(messageType, TwitchWebsocketMessageType):
            raise TypeError(f'messageType argument is malformed: \"{messageType}\"')
        elif subscriptionType is not None and not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

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
