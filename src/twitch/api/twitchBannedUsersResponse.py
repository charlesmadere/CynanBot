from dataclasses import dataclass

from .twitchBannedUser import TwitchBannedUser


@dataclass(frozen = True)
class TwitchBannedUsersResponse:
    users: list[TwitchBannedUser] | None
    broadcasterId: str
    requestedUserId: str | None
