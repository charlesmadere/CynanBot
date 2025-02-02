from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchRaid:
    viewerCount: int
    profileImageUrl: str | None
    userId: str
    userLogin: str
    userName: str
