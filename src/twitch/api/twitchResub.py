from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchResub():
    gifterIsAnonymous: bool | None
    isGift: bool
    cumulativeMonths: int
    durationMonths: int
    streakMonths: int
    gifterUserId: str | None
    gifterUserLogin: str | None
    gifterUserName: str | None
    subTier: TwitchSubscriberTier
