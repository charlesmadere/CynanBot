from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchSendChatDropReason:
    code: str | None
    message: str | None
