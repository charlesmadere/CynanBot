from abc import ABC, abstractmethod

from .eccoTimeRemainingType import EccoTimeRemainingType


class AbsEccoTimeRemaining(ABC):

    @property
    @abstractmethod
    def timeRemainingType(self) -> EccoTimeRemainingType:
        pass
