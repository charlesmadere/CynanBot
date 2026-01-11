from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


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
