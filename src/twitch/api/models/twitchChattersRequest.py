from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChattersRequest:
    first: int
    broadcasterId: str
    moderatorId: str
