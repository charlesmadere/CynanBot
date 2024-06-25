from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchSendChatDropReason():
    code: str
    message: str | None
