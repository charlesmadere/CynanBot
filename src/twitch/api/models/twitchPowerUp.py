from dataclasses import dataclass

from .twitchPowerUpEmote import TwitchPowerUpEmote
from .twitchPowerUpType import TwitchPowerUpType


@dataclass(frozen = True, slots = True)
class TwitchPowerUp:
    messageEffectId: str | None
    powerUpEmote: TwitchPowerUpEmote | None
    powerUpType: TwitchPowerUpType
