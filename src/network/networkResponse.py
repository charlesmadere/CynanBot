from abc import ABC, abstractmethod
from typing import Any

from .networkClientType import NetworkClientType


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
    async def json(self) -> dict[str, Any] | list[Any] | None:
        pass

    @abstractmethod
    async def read(self) -> bytes:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def xml(self) -> dict[str, Any] | list[Any] | None:
        pass
