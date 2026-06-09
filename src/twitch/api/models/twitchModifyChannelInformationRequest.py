from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchModifyChannelInformationRequest:
    gameId: str | None
    title: str | None
    twitchChannelId: str
