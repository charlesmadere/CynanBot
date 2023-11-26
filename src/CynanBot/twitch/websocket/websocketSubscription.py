from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketConnectionStatus import \
    WebsocketConnectionStatus
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport


class WebsocketSubscription():

    def __init__(
        self,
        cost: int,
        createdAt: SimpleDateTime,
        subscriptionId: str,
        version: str,
        condition: WebsocketCondition,
        status: WebsocketConnectionStatus,
        subscriptionType: WebsocketSubscriptionType,
        transport: WebsocketTransport
    ):
        if not utils.isValidInt(cost):
            raise ValueError(f'cost argument is malformed: \"{cost}\"')
        elif not isinstance(createdAt, SimpleDateTime):
            raise ValueError(f'createdAt argument is malformed: \"{createdAt}\"')
        elif not utils.isValidStr(subscriptionId):
            raise ValueError(f'subscriptionId argument is malformed: \"{subscriptionId}\"')
        elif not utils.isValidStr(version):
            raise ValueError(f'version argument is malformed: \"{version}\"')
        elif not isinstance(condition, WebsocketCondition):
            raise ValueError(f'condition argument is malformed: \"{condition}\"')
        elif not isinstance(status, WebsocketConnectionStatus):
            raise ValueError(f'status argument is malformed: \"{status}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(transport, WebsocketTransport):
            raise ValueError(f'transport argument is malformed: \"{transport}\"')

        self.__cost: int = cost
        self.__createdAt: SimpleDateTime = createdAt
        self.__subscriptionId: str = subscriptionId
        self.__version: str = version
        self.__condition: WebsocketCondition = condition
        self.__status: WebsocketConnectionStatus = status
        self.__subscriptionType: WebsocketSubscriptionType = subscriptionType
        self.__transport: WebsocketTransport = transport

    def getCondition(self) -> WebsocketCondition:
        return self.__condition

    def getCost(self) -> int:
        return self.__cost

    def getCreatedAt(self) -> SimpleDateTime:
        return self.__createdAt

    def getStatus(self) -> WebsocketConnectionStatus:
        return self.__status

    def getSubscriptionId(self) -> str:
        return self.__subscriptionId

    def getSubscriptionType(self) -> WebsocketSubscriptionType:
        return self.__subscriptionType

    def getTransport(self) -> WebsocketTransport:
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
