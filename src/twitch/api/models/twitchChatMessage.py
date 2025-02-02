from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchChatMessageFragment import TwitchChatMessageFragment


@dataclass(frozen = True)
class TwitchChatMessage:
    fragments: FrozenList[TwitchChatMessageFragment]
    text: str
