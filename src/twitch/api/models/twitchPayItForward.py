from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchPayItForward:
    gifterIsAnonymous: bool
    gifterUserId: str | None
    gifterUserLogin: str | None
    gifterUserName: str | None
