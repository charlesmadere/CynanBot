from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchBroadcasterSubscription import TwitchBroadcasterSubscription
from .twitchPaginationResponse import TwitchPaginationResponse


@dataclass(frozen = True)
class TwitchBroadcasterSubscriptionsResponse:
    data: FrozenList[TwitchBroadcasterSubscription]
    points: int
    total: int
    pagination: TwitchPaginationResponse | None
