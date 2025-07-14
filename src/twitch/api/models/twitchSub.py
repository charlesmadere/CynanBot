from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchSub:
    isPrime: bool
    durationMonths: int
    subTier: TwitchSubscriberTier
