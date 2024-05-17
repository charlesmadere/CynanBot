from dataclasses import dataclass
from datetime import datetime

from CynanBot.twitch.api.websocket.twitchWebsocketMessageType import \
    TwitchWebsocketMessageType
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType


@dataclass(frozen = True)
class TwitchWebsocketMetadata():
    messageTimestamp: datetime
    messageId: str
    subscriptionVersion: str | None
    messageType: TwitchWebsocketMessageType | None
    subscriptionType: TwitchWebsocketSubscriptionType | None
