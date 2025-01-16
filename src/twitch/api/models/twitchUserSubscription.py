from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


# This class intends to directly correspond to Twitch's "Check User Subscription" API:
# https://dev.twitch.tv/docs/api/reference/#check-user-subscription
@dataclass(frozen = True)
class TwitchUserSubscription:
    isGift: bool
    broadcasterId: str
    broadcasterLogin: str
    broadcasterName: str
    gifterId: str | None
    gifterLogin: str | None
    gifterName: str | None
    tier: TwitchSubscriberTier
