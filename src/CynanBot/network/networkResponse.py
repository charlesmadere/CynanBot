from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from CynanBot.network.networkClientType import NetworkClientType


class NetworkResponse(ABC):

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    def getNetworkClientType(self) -> NetworkClientType:
        pass

    @abstractmethod
    def getStatusCode(self) -> int:
        pass

    @abstractmethod
    def getUrl(self) -> str:
        pass

    @abstractmethod
    def isClosed(self) -> bool:
        pass

    @abstractmethod
    async def json(self) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def read(self) -> bytes:
        pass
