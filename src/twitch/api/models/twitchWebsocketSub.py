from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TwitchWebsocketSub:
    isPrime: bool
    durationMonths: int
    subTier: TwitchSubscriberTier
