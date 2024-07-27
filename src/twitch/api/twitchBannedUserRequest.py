from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchBannedUserRequest:
    broadcasterId: str
    requestedUserId: str | None
