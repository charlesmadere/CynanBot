from dataclasses import dataclass


# This class intends to directly correspond to Twitch's "Unban User" API:
# https://dev.twitch.tv/docs/api/reference/#unban-user
@dataclass(frozen = True, slots = True)
class TwitchUnbanRequest:
    broadcasterUserId: str
    moderatorUserId: str
    userIdToBan: str
