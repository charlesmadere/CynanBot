from abc import ABC, abstractmethod
from typing import Any, List, Optional

from CynanBot.storage.databaseType import DatabaseType


class DatabaseConnection(ABC):

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def createTableIfNotExists(self, query: str, *args: Optional[Any]):
        pass

    @abstractmethod
    async def execute(self, query: str, *args: Optional[Any]):
        pass

    @abstractmethod
    async def fetchRow(self, query: str, *args: Optional[Any]) -> Optional[List[Any]]:
        pass

    @abstractmethod
    async def fetchRows(self, query: str, *args: Optional[Any]) -> Optional[List[List[Any]]]:
        pass

    @abstractmethod
    def getDatabaseType(self) -> DatabaseType:
        pass

    @abstractmethod
    def isClosed(self) -> bool:
        pass
