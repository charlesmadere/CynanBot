from abc import ABC, abstractmethod
from datetime import datetime


class EccoApiServiceInterface(ABC):

    @abstractmethod
    async def fetchEccoTimerDateTime(self) -> datetime:
        pass
