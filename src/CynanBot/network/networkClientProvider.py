from abc import ABC, abstractmethod

from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkHandle import NetworkHandle


class NetworkClientProvider(ABC):

    @abstractmethod
    async def get(self) -> NetworkHandle:
        pass

    @abstractmethod
    def getNetworkClientType(self) -> NetworkClientType:
        pass
