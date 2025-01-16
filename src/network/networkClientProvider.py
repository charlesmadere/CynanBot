from abc import ABC, abstractmethod

from .networkClientType import NetworkClientType
from .networkHandle import NetworkHandle


class NetworkClientProvider(ABC):

    @abstractmethod
    async def get(self) -> NetworkHandle:
        pass

    @property
    @abstractmethod
    def networkClientType(self) -> NetworkClientType:
        pass
