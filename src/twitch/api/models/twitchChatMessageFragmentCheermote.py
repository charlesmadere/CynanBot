from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragmentCheermote:
    bits: int
    tier: int
    prefix: str
