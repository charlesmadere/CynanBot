from dataclasses import dataclass

from .twitchWebsocketEvent import TwitchWebsocketEvent
from .twitchWebsocketSession import TwitchWebsocketSession
from .twitchWebsocketSubscription import TwitchWebsocketSubscription


@dataclass(frozen = True)
class TwitchWebsocketPayload:
    event: TwitchWebsocketEvent | None
    session: TwitchWebsocketSession | None
    subscription: TwitchWebsocketSubscription | None

    def requireSubscription(self) -> TwitchWebsocketSubscription:
        if self.subscription is None:
            raise RuntimeError(f'this TwitchWebsocketPayload has no subscription ({self})')

        return self.subscription
