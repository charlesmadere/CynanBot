from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport


class TwitchWebsocketSubscription():

    def __init__(
        self,
        cost: int,
        createdAt: SimpleDateTime,
        subscriptionId: str,
        version: str,
        condition: TwitchWebsocketCondition,
        status: TwitchWebsocketConnectionStatus,
        subscriptionType: TwitchWebsocketSubscriptionType,
        transport: TwitchWebsocketTransport
    ):
        if not utils.isValidInt(cost):
            raise ValueError(f'cost argument is malformed: \"{cost}\"')
        assert isinstance(createdAt, SimpleDateTime), f"malformed {createdAt=}"
        if not utils.isValidStr(subscriptionId):
            raise ValueError(f'subscriptionId argument is malformed: \"{subscriptionId}\"')
        if not utils.isValidStr(version):
            raise ValueError(f'version argument is malformed: \"{version}\"')
        assert isinstance(condition, TwitchWebsocketCondition), f"malformed {condition=}"
        assert isinstance(status, TwitchWebsocketConnectionStatus), f"malformed {status=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"
        assert isinstance(transport, TwitchWebsocketTransport), f"malformed {transport=}"

        self.__cost: int = cost
        self.__createdAt: SimpleDateTime = createdAt
        self.__subscriptionId: str = subscriptionId
        self.__version: str = version
        self.__condition: TwitchWebsocketCondition = condition
        self.__status: TwitchWebsocketConnectionStatus = status
        self.__subscriptionType: TwitchWebsocketSubscriptionType = subscriptionType
        self.__transport: TwitchWebsocketTransport = transport

    def getCondition(self) -> TwitchWebsocketCondition:
        return self.__condition

    def getCost(self) -> int:
        return self.__cost

    def getCreatedAt(self) -> SimpleDateTime:
        return self.__createdAt

    def getStatus(self) -> TwitchWebsocketConnectionStatus:
        return self.__status

    def getSubscriptionId(self) -> str:
        return self.__subscriptionId

    def getSubscriptionType(self) -> TwitchWebsocketSubscriptionType:
        return self.__subscriptionType

    def getTransport(self) -> TwitchWebsocketTransport:
        return self.__transport

    def getVersion(self) -> str:
        return self.__version

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'condition': self.__condition,
            'cost': self.__cost,
            'createdAt': self.__createdAt,
            'status': self.__status,
            'subscriptionId': self.__subscriptionId,
            'subscriptionType': self.__subscriptionType,
            'transport': self.__transport.toDictionary(),
            'version': self.__version
        }
