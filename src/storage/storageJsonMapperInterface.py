from abc import ABC, abstractmethod
from typing import Any

from .databaseType import DatabaseType


class StorageJsonMapperInterface(ABC):

    @abstractmethod
    def parseDatabaseType(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType | None:
        pass

    @abstractmethod
    async def parseDatabaseTypeAsync(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType | None:
        pass

    @abstractmethod
    def requireDatabaseType(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        pass

    @abstractmethod
    async def requireDatabaseTypeAsync(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        pass
