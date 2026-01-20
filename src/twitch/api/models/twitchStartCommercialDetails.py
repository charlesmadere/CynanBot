from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchStartCommercialDetails:
    length: int
    retryAfter: int | None
    message: str | None
