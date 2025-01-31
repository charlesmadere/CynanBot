from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChattersRequest:
    first: int | None
    broadcasterId: str
    moderatorId: str
