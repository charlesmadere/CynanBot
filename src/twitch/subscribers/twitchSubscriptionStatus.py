from dataclasses import dataclass

from ..api.models.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True, slots = True)
class TwitchSubscriptionStatus:
    isGift: bool
    broadcasterId: str
    broadcasterLogin: str
    broadcasterName: str
    gifterId: str | None
    gifterLogin: str | None
    gifterName: str | None
    userId: str
    tier: TwitchSubscriberTier
