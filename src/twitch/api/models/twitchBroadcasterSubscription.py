from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True, slots = True)
class TwitchBroadcasterSubscription:
    isGift: bool
    broadcasterId: str
    broadcasterLogin: str
    broadcasterName: str
    gifterId: str | None
    gifterLogin: str | None
    gifterName: str | None
    planName: str | None
    userId: str
    userLogin: str
    userName: str
    tier: TwitchSubscriberTier
