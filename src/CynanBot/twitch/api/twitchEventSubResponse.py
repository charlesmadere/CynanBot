from dataclasses import dataclass
from datetime import datetime

from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport


@dataclass(frozen = True)
class TwitchEventSubResponse():
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
