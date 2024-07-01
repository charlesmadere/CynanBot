from dataclasses import dataclass

from CynanBot.twitch.api.twitchEmoteImageFormat import TwitchEmoteImageFormat
from CynanBot.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from CynanBot.twitch.api.twitchEmoteType import TwitchEmoteType
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.twitchThemeMode import TwitchThemeMode


@dataclass(frozen = True)
class TwitchEmoteDetails():
    images: dict[TwitchEmoteImageScale, str]
    scales: set[TwitchEmoteImageScale]
    formats: set[TwitchEmoteImageFormat]
    themeModes: set[TwitchThemeMode]
    emoteId: str
    emoteSetId: str
    name: str
    emoteType: TwitchEmoteType
    tier: TwitchSubscriberTier
