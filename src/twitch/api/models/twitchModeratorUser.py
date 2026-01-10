from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchModeratorUser:
    userId: str
    userLogin: str
    userName: str
