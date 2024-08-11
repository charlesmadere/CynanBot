from dataclasses import dataclass

from .twitchBroadcasterSusbcription import TwitchBroadcasterSubscription


@dataclass(frozen = True)
class TwitchBroadcasterSubscriptions:
    points: int
    total: int
    subscription: TwitchBroadcasterSubscription | None