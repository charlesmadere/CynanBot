from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


# This class intends to directly correspond to Twitch's "Get Broadcaster Subscriptions" API:
# https://dev.twitch.tv/docs/api/reference/#get-broadcaster-subscriptions
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
    userId: str
    userName: str
    userLogin: str
