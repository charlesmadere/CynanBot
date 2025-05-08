from .absEccoTimeRemaining import AbsEccoTimeRemaining
from .eccoTimeRemainingType import EccoTimeRemainingType


class EccoReleased(AbsEccoTimeRemaining):

    @property
    def timeRemainingType(self) -> EccoTimeRemainingType:
        return EccoTimeRemainingType.RELEASED
