from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchModUser:
    userId: str
    userLogin: str
    userName: str
