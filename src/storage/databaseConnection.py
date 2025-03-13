from abc import ABC, abstractmethod
from typing import Any

from frozenlist import FrozenList

from .databaseType import DatabaseType


class DatabaseConnection(ABC):

    @abstractmethod
    async def close(self):
        pass

    @property
    @abstractmethod
    def databaseType(self) -> DatabaseType:
        pass

    @abstractmethod
    async def execute(self, query: str, *args: Any | None):
        pass

    @abstractmethod
    async def fetchRow(self, query: str, *args: Any | None) -> FrozenList[Any] | None:
        pass

    @abstractmethod
    async def fetchRows(self, query: str, *args: Any | None) -> FrozenList[FrozenList[Any]] | None:
        pass

    @property
    @abstractmethod
    def isClosed(self) -> bool:
        pass
