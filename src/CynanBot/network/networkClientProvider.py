from abc import ABC, abstractmethod

from network.networkClientType import NetworkClientType
from network.networkHandle import NetworkHandle


class NetworkClientProvider(ABC):

    @abstractmethod
    async def get(self) -> NetworkHandle:
        pass

    @abstractmethod
    def getNetworkClientType(self) -> NetworkClientType:
        pass
