from dataclasses import dataclass

from .twitchEmoteImageFormat import TwitchEmoteImageFormat


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragmentEmote:
    imageFormats: frozenset[TwitchEmoteImageFormat] | None
    emoteId: str
    emoteSetId: str
    ownerId: str
