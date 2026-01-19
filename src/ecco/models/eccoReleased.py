from dataclasses import dataclass

from .absEccoTimeRemaining import AbsEccoTimeRemaining


@dataclass(frozen = True)
class EccoReleased(AbsEccoTimeRemaining):

    pass
