from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragmentGif:
    gifId: str
    url: str
