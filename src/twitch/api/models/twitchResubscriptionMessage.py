from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchResubscriptionMessageEmote import TwitchResubscriptionMessageEmote


@dataclass(frozen = True, slots = True)
class TwitchResubscriptionMessage:
    emotes: FrozenList[TwitchResubscriptionMessageEmote] | None
    text: str
