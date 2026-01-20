from dataclasses import dataclass

from frozendict import frozendict

from .twitchEmoteImageFormat import TwitchEmoteImageFormat
from .twitchEmoteImageScale import TwitchEmoteImageScale
from .twitchEmoteType import TwitchEmoteType
from .twitchSubscriberTier import TwitchSubscriberTier
from .twitchThemeMode import TwitchThemeMode


@dataclass(frozen = True, slots = True)
class TwitchEmoteDetails:
    images: frozendict[TwitchEmoteImageScale, str]
    formats: frozenset[TwitchEmoteImageFormat]
    scales: frozenset[TwitchEmoteImageScale]
    themeModes: frozenset[TwitchThemeMode]
    emoteId: str
    emoteSetId: str
    name: str
    emoteType: TwitchEmoteType
    tier: TwitchSubscriberTier | None
