from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchResubscriptionMessageEmote:
    begin: int
    end: int
    emoteId: str
