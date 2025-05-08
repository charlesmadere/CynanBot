from abc import ABC, abstractmethod

from .models.eccoTimerData import EccoTimerData


class EccoApiServiceInterface(ABC):

    @abstractmethod
    async def fetchEccoTimerData(self) -> EccoTimerData:
        pass
