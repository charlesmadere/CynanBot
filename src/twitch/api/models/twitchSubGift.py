from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True, slots = True)
class TwitchSubGift:
    cumulativeTotal: int | None
    durationMonths: int
    communityGiftId: str | None
    recipientUserId: str
    recipientUserLogin: str
    recipientUserName: str
    subTier: TwitchSubscriberTier
