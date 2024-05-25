from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChatDropReason():
    code: str
    message: str | None
