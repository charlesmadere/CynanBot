from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChatMessageFragmentMention:
    userId: str
    userLogin: str
    userName: str
