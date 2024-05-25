from dataclasses import dataclass

from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchSubGift():
    cumulativeTotal: int | None
    durationMonths: int
    communityGiftId: str | None
    recipientUserId: str
    recipientUserLogin: str
    recipientUserName: str
    subTier: TwitchSubscriberTier
