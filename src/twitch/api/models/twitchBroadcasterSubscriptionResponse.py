from dataclasses import dataclass

from .twitchBroadcasterSubscription import TwitchBroadcasterSubscription


@dataclass(frozen = True)
class TwitchBroadcasterSubscriptionResponse:
    points: int
    total: int
    subscription: TwitchBroadcasterSubscription | None
