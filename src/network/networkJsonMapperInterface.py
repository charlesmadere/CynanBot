from abc import ABC, abstractmethod
from typing import Any

from .networkClientType import NetworkClientType


class NetworkJsonMapperInterface(ABC):

    @abstractmethod
    def parseClientType(
        self,
        clientType: str | Any | None,
    ) -> NetworkClientType:
        pass

    @abstractmethod
    async def parseClientTypeAsync(
        self,
        clientType: str | Any | None,
    ) -> NetworkClientType:
        pass

    @abstractmethod
    def serializeClientType(
        self,
        clientType: NetworkClientType,
    ) -> str:
        pass
