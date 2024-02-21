import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType


class TwitchEventSubResponse():

    def __init__(
        self,
        cost: int,
        maxTotalCost: int,
        total: int,
        totalCost: int,
        createdAt: SimpleDateTime,
        subscriptionId: str,
        version: str,
        condition: TwitchWebsocketCondition,
        subscriptionType: TwitchWebsocketSubscriptionType,
        status: TwitchWebsocketConnectionStatus,
        transport: TwitchWebsocketTransport
    ):
        if not utils.isValidInt(cost):
            raise ValueError(f'cost argument is malformed: \"{cost}\"')
        elif not utils.isValidInt(maxTotalCost):
            raise ValueError(f'maxTotalCost argument is malformed: \"{maxTotalCost}\"')
        elif not utils.isValidInt(total):
            raise ValueError(f'total argument is malformed: \"{total}\"')
        elif not utils.isValidInt(totalCost):
            raise ValueError(f'totalCost argument is malformed: \"{totalCost}\"')
        elif not isinstance(createdAt, SimpleDateTime):
            raise ValueError(f'createdAt argument is malformed: \"{createdAt}\"')
        elif not utils.isValidStr(subscriptionId):
            raise ValueError(f'subscriptionId argument is malformed: \"{subscriptionId}\"')
        elif not utils.isValidStr(version):
            raise ValueError(f'version argument is malformed: \"{version}\"')
        elif not isinstance(condition, TwitchWebsocketCondition):
            raise ValueError(f'condition argument is malformed: \"{condition}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(status, TwitchWebsocketConnectionStatus):
            raise ValueError(f'status argument is malformed: \"{status}\"')
        elif not isinstance(transport, TwitchWebsocketTransport):
            raise ValueError(f'transport argument is malformed: \"{transport}\"')

        self.__cost: int = cost
        self.__maxTotalCost: int = maxTotalCost
        self.__total: int = total
        self.__totalCost: int = totalCost
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

    def getMaxTotalCost(self) -> int:
        return self.__maxTotalCost

    def getStatus(self) -> TwitchWebsocketConnectionStatus:
        return self.__status

    def getSubscriptionId(self) -> str:
        return self.__subscriptionId

    def getSubscriptionType(self) -> TwitchWebsocketSubscriptionType:
        return self.__subscriptionType

    def getTotal(self) -> int:
        return self.__total

    def getTotalCost(self) -> int:
        return self.__totalCost

    def getTransport(self) -> TwitchWebsocketTransport:
        return self.__transport

    def getVersion(self) -> str:
        return self.__version

    def __str__(self) -> str:
        return f'condition=\"{self.__condition}\", cost=\"{self.__cost}\", createdAt=\"{self.__createdAt}\", maxTotalCost=\"{self.__maxTotalCost}\" \
            status=\"{self.__status}\", subscriptionId=\"{self.__subscriptionId}\", subscriptionType=\"{self.__subscriptionType}\" \
            total=\"{self.__total}\", totalCost=\"{self.__totalCost}\", transport=\"{self.__transport}\", version=\"{self.__version}\"'
