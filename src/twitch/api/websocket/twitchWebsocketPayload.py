from dataclasses import dataclass

from .twitchWebsocketEvent import TwitchWebsocketEvent
from .twitchWebsocketSession import TwitchWebsocketSession
from .twitchWebsocketSubscription import TwitchWebsocketSubscription


@dataclass(frozen = True)
class TwitchWebsocketPayload():
    event: TwitchWebsocketEvent | None = None
    session: TwitchWebsocketSession | None = None
    subscription: TwitchWebsocketSubscription | None = None

    def isEmpty(self) -> bool:
        return self.event is None and self.session is None and self.subscription is None

    def requireSubscription(self) -> TwitchWebsocketSubscription:
        if self.subscription is None:
            raise ValueError(f'this WebsocketPayload has no subscription ({self})')

        return self.subscription
