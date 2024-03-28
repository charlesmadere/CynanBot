from abc import ABC, abstractmethod
from typing import Any

from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkResponse import NetworkResponse


class NetworkHandle(ABC):

    @abstractmethod
    async def delete(
        self,
        url: str,
        headers: dict[str, Any] | None = None
    ) -> NetworkResponse:
        pass

    @abstractmethod
    async def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None
    ) -> NetworkResponse:
        pass

    @abstractmethod
    def getNetworkClientType(self) -> NetworkClientType:
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None
    ) -> NetworkResponse:
        pass
