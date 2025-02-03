from dataclasses import dataclass

from .twitchEmoteImageFormat import TwitchEmoteImageFormat


@dataclass(frozen = True)
class TwitchChatMessageFragmentEmote:
    formats: frozenset[TwitchEmoteImageFormat] | None
    emoteId: str
    emoteSetId: str
    ownerId: str
