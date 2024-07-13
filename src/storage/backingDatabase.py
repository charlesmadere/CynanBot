from abc import ABC, abstractmethod

from .databaseConnection import DatabaseConnection
from .databaseType import DatabaseType


class BackingDatabase(ABC):

    @property
    @abstractmethod
    def databaseType(self) -> DatabaseType:
        pass

    @abstractmethod
    async def getConnection(self) -> DatabaseConnection:
        pass
