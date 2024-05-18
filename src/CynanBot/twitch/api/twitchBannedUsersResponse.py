from dataclasses import dataclass

from CynanBot.twitch.api.twitchBannedUser import TwitchBannedUser


@dataclass(frozen = True)
class TwitchBannedUsersResponse():
    users: list[TwitchBannedUser] | None
    broadcasterId: str
    requestedUserId: str | None
