from abc import ABC, abstractmethod

from .models.absEccoTimeRemaining import AbsEccoTimeRemaining


class EccoHelperInterface(ABC):

    @abstractmethod
    async def fetchEccoTimeRemaining(self) -> AbsEccoTimeRemaining:
        pass
