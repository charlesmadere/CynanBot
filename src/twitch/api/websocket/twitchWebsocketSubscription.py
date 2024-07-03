from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketCondition import TwitchWebsocketCondition
from .twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from .twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .twitchWebsocketTransport import TwitchWebsocketTransport


@dataclass(frozen = True)
class TwitchWebsocketSubscription():
    createdAt: datetime
    cost: int
    subscriptionId: str
    version: str
    condition: TwitchWebsocketCondition
    status: TwitchWebsocketConnectionStatus
    subscriptionType: TwitchWebsocketSubscriptionType
    transport: TwitchWebsocketTransport
