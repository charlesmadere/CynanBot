from dataclasses import dataclass

from .twitchEmoteImageFormat import TwitchEmoteImageFormat
from .twitchEmoteImageScale import TwitchEmoteImageScale
from .twitchEmoteType import TwitchEmoteType
from .twitchSubscriberTier import TwitchSubscriberTier
from .twitchThemeMode import TwitchThemeMode


@dataclass(frozen = True)
class TwitchEmoteDetails:
    images: dict[TwitchEmoteImageScale, str]
    formats: frozenset[TwitchEmoteImageFormat]
    scales: frozenset[TwitchEmoteImageScale]
    themeModes: frozenset[TwitchThemeMode]
    emoteId: str
    emoteSetId: str
    name: str
    emoteType: TwitchEmoteType
    tier: TwitchSubscriberTier
