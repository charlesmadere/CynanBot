from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchGiftPaidUpgrade:
    gifterIsAnonymous: bool
    gifterUserId: str | None
    gifterUserName: str | None
