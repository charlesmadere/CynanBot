from dataclasses import dataclass
from datetime import datetime

from .twitchWebsocketMessageType import TwitchWebsocketMessageType
from .twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType


@dataclass(frozen = True)
class TwitchWebsocketMetadata:
    messageTimestamp: datetime
    messageId: str
    subscriptionVersion: str | None
    messageType: TwitchWebsocketMessageType
    subscriptionType: TwitchWebsocketSubscriptionType | None
