from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChatMessageFragmentCheermote:
    bits: int
    tier: int
    prefix: str
