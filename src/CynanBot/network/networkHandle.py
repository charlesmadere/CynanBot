from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from network.networkClientType import NetworkClientType
from network.networkResponse import NetworkResponse


class NetworkHandle(ABC):

    @abstractmethod
    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        pass

    @abstractmethod
    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        pass

    @abstractmethod
    def getNetworkClientType(self) -> NetworkClientType:
        pass

    @abstractmethod
    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        pass
