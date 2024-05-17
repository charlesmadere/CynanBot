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
class TwitchWebsocketSubscription():
    createdAt: datetime
    cost: int
    subscriptionId: str
    version: str
    condition: TwitchWebsocketCondition
    status: TwitchWebsocketConnectionStatus
    subscriptionType: TwitchWebsocketSubscriptionType
    transport: TwitchWebsocketTransport
