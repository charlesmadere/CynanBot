from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketCondition import TwitchWebsocketCondition
from .twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from .twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .twitchWebsocketTransport import TwitchWebsocketTransport


@dataclass(frozen = True)
class TwitchEventSubDetails:
    createdAt: datetime
    cost: int
    detailsId: str
    version: str
    condition: TwitchWebsocketCondition
    connectionStatus: TwitchWebsocketConnectionStatus
    subscriptionType: TwitchWebsocketSubscriptionType
    transport: TwitchWebsocketTransport
