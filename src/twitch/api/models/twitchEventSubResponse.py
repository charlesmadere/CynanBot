from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketCondition import TwitchWebsocketCondition
from .twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from .twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .twitchWebsocketTransport import TwitchWebsocketTransport


@dataclass(frozen = True)
class TwitchEventSubResponse:
    createdAt: datetime
    cost: int
    maxTotalCost: int
    total: int
    totalCost: int
    subscriptionId: str
    version: str
    condition: TwitchWebsocketCondition
    subscriptionType: TwitchWebsocketSubscriptionType
    status: TwitchWebsocketConnectionStatus
    transport: TwitchWebsocketTransport
