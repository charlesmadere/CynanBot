from abc import ABC, abstractmethod
from typing import Any

from .databaseType import DatabaseType


class DatabaseConnection(ABC):

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def createTableIfNotExists(self, query: str, *args: Any | None):
        pass

    @abstractmethod
    async def execute(self, query: str, *args: Any | None):
        pass

    @abstractmethod
    async def fetchRow(self, query: str, *args: Any | None) -> list[Any] | None:
        pass

    @abstractmethod
    async def fetchRows(self, query: str, *args: Any | None) -> list[list[Any]] | None:
        pass

    @abstractmethod
    def getDatabaseType(self) -> DatabaseType:
        pass

    @abstractmethod
    def isClosed(self) -> bool:
        pass
