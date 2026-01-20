from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchPaginationResponse:
    cursor: str
