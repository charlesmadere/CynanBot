from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchCategoryOrGameEntry:
    boxArtUrl: str | None
    categoryOrGameId: str
    categoryOrGameName: str
