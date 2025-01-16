from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchPaginationResponse:
    cursor: str
