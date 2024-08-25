from dataclasses import dataclass

from .twitchBannedUser import TwitchBannedUser


# This class intends to directly correspond to Twitch's "Get Banned Users" API:
# https://dev.twitch.tv/docs/api/reference/#get-banned-users
@dataclass(frozen = True)
class TwitchBannedUserResponse:
    bannedUser: TwitchBannedUser | None = None
