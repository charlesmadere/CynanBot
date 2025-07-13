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

    def requireSubscriptionType(self) -> TwitchWebsocketSubscriptionType:
        if self.subscriptionType is None:
            raise RuntimeError(f'this TwitchWebsocketMetadata has no subscriptionType ({self})')

        return self.subscriptionType
