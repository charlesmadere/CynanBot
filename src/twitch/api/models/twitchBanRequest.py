from dataclasses import dataclass


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
@dataclass(frozen = True, slots = True)
class TwitchBanRequest:
    duration: int | None
    broadcasterUserId: str
    moderatorUserId: str
    reason: str | None
    userIdToBan: str
