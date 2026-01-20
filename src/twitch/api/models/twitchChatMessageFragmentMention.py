from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchChatMessageFragmentMention:
    userId: str
    userLogin: str
    userName: str
