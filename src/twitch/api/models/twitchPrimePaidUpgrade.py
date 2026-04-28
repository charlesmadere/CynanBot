from dataclasses import dataclass

from .twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True, slots = True)
class TwitchPrimePaidUpgrade:
    subTier: TwitchSubscriberTier
