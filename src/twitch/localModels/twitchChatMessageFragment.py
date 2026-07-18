from dataclasses import dataclass

from .twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote
from .twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote
from .twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif
from .twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention
from .twitchChatMessageFragmentType import TwitchChatMessageFragmentType


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragment:
    text: str
    cheermote: TwitchChatMessageFragmentCheermote | None
    emote: TwitchChatMessageFragmentEmote | None
    gif: TwitchChatMessageFragmentGif | None
    mention: TwitchChatMessageFragmentMention | None
    fragmentType: TwitchChatMessageFragmentType
