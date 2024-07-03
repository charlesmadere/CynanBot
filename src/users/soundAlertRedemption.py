from dataclasses import dataclass

from ..soundPlayerManager.soundAlert import SoundAlert


@dataclass(frozen = True)
class SoundAlertRedemption():
    isImmediate: bool
    soundAlert: SoundAlert
    directoryPath: str | None
    rewardId: str
