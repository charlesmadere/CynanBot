from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchGame:
    boxArtUrl: str | None
    gameId: str
    gameName: str
    igdbId: str | None
