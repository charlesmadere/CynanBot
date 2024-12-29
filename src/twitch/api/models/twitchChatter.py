from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchChatter:
    userId: str
    userLogin: str
    userName: str
