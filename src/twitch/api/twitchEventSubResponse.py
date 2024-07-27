from dataclasses import dataclass
from datetime import datetime

from .websocket.twitchWebsocketCondition import TwitchWebsocketCondition
from .websocket.twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from .websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .websocket.twitchWebsocketTransport import TwitchWebsocketTransport


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
