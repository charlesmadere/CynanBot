from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchStartCommercialDetails:
    length: int
    retryAfter: int | None
    message: str | None
