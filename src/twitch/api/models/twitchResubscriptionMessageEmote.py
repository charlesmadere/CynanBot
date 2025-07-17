from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchResubscriptionMessageEmote:
    begin: int
    end: int
    emoteId: str
