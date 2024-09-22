from abc import ABC, abstractmethod
from typing import Any

from .networkClientType import NetworkClientType


class NetworkResponse(ABC):

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    def isClosed(self) -> bool:
        pass

    @abstractmethod
    async def json(self) -> dict[str, Any] | list[Any] | None:
        pass

    @property
    @abstractmethod
    def networkClientType(self) -> NetworkClientType:
        pass

    @abstractmethod
    async def read(self) -> bytes | None:
        pass

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @property
    @abstractmethod
    def statusCode(self) -> int:
        pass

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    async def xml(self) -> dict[str, Any] | list[Any] | None:
        pass
