from dataclasses import dataclass
from datetime import datetime

from .absEccoTimeRemaining import AbsEccoTimeRemaining


@dataclass(frozen = True, slots = True)
class EccoTimeRemaining(AbsEccoTimeRemaining):
    timerDateTime: datetime
    remainingSeconds: int
