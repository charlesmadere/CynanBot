from dataclasses import dataclass

from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchCommunitySubGift():
    cumulativeTotal: int | None
    total: int
    communitySubGiftId: str
    subTier: TwitchSubscriberTier
