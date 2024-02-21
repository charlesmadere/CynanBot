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
        if not utils.isValidInt(maxTotalCost):
            raise ValueError(f'maxTotalCost argument is malformed: \"{maxTotalCost}\"')
        if not utils.isValidInt(total):
            raise ValueError(f'total argument is malformed: \"{total}\"')
        if not utils.isValidInt(totalCost):
            raise ValueError(f'totalCost argument is malformed: \"{totalCost}\"')
        assert isinstance(createdAt, SimpleDateTime), f"malformed {createdAt=}"
        if not utils.isValidStr(subscriptionId):
            raise ValueError(f'subscriptionId argument is malformed: \"{subscriptionId}\"')
        if not utils.isValidStr(version):
            raise ValueError(f'version argument is malformed: \"{version}\"')
        assert isinstance(condition, TwitchWebsocketCondition), f"malformed {condition=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"
        assert isinstance(status, TwitchWebsocketConnectionStatus), f"malformed {status=}"
        assert isinstance(transport, TwitchWebsocketTransport), f"malformed {transport=}"

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
