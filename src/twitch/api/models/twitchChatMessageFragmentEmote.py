from dataclasses import dataclass

from .twitchEmoteImageFormat import TwitchEmoteImageFormat


@dataclass(frozen = True)
class TwitchChatMessageFragmentEmote:
    emoteSetId: str
    fragmentEmoteId: str
    ownerId: str
    format: TwitchEmoteImageFormat
