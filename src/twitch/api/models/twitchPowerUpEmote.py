from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchPowerUpEmote:
    emoteId: str
    emoteName: str
