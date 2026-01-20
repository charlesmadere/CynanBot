from dataclasses import dataclass

from .absEccoTimeRemaining import AbsEccoTimeRemaining


@dataclass(frozen = True, slots = True)
class EccoReleased(AbsEccoTimeRemaining):

    pass
