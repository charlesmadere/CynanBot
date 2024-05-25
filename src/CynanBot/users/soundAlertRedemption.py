from dataclasses import dataclass

from CynanBot.soundPlayerManager.soundAlert import SoundAlert


@dataclass(frozen = True)
class SoundAlertRedemption():
    soundAlert: SoundAlert
    rewardId: str
