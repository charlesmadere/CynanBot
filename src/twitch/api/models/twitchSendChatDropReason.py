from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchSendChatDropReason:
    code: str | None
    message: str | None
