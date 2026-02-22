from dataclasses import dataclass

from .twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote
from .twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote
from .twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention
from .twitchChatMessageFragmentType import TwitchChatMessageFragmentType


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragment:
    text: str
    cheermote: TwitchChatMessageFragmentCheermote | None
    emote: TwitchChatMessageFragmentEmote | None
    mention: TwitchChatMessageFragmentMention | None
    fragmentType: TwitchChatMessageFragmentType
