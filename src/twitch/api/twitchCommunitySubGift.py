from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchCommunitySubGift():
    cumulativeTotal: int | None
    total: int
    communitySubGiftId: str
    subTier: TwitchSubscriberTier
