from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchUserSubscription import TwitchUserSubscription


# This class intends to directly correspond to Twitch's "Check User Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#check-user-subscription
@dataclass(frozen = True, slots = True)
class TwitchUserSubscriptionsResponse:
    data: FrozenList[TwitchUserSubscription]
