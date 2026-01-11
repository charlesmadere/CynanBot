from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchBroadcasterSubscription import TwitchBroadcasterSubscription
from .twitchPaginationResponse import TwitchPaginationResponse


# This class intends to directly correspond to Twitch's "Check User Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#get-broadcaster-subscriptions
@dataclass(frozen = True)
class TwitchBroadcasterSubscriptionsResponse:
    data: FrozenList[TwitchBroadcasterSubscription]
    points: int
    total: int
    pagination: TwitchPaginationResponse | None
