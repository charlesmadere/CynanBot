from dataclasses import dataclass

from .twitchBannedUser import TwitchBannedUser
from .twitchPaginationResponse import TwitchPaginationResponse


@dataclass(frozen = True)
class TwitchBannedUsersPageResponse:
    users: list[TwitchBannedUser] | None
    pagination: TwitchPaginationResponse | None
