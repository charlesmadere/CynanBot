from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchPowerUpEmote:
    emoteId: str
    emoteName: str
