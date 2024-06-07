from dataclasses import dataclass

from CynanBot.twitch.api.twitchBannedUser import TwitchBannedUser
from CynanBot.twitch.api.twitchPaginationResponse import \
    TwitchPaginationResponse


@dataclass(frozen = True)
class TwitchBannedUsersPageResponse():
    users: list[TwitchBannedUser] | None
    pagination: TwitchPaginationResponse | None
