from dataclasses import dataclass
from datetime import datetime

from .absEccoTimeRemaining import AbsEccoTimeRemaining
from .eccoTimeRemainingType import EccoTimeRemainingType


@dataclass(frozen = True)
class EccoTimeRemaining(AbsEccoTimeRemaining):
    timerDateTime: datetime
    remainingSeconds: int

    @property
    def timeRemainingType(self) -> EccoTimeRemainingType:
        return EccoTimeRemainingType.TIME_REMAINING
