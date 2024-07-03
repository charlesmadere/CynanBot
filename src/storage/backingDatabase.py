from abc import ABC, abstractmethod

from .databaseConnection import DatabaseConnection
from .databaseType import DatabaseType


class BackingDatabase(ABC):

    @abstractmethod
    async def getConnection(self) -> DatabaseConnection:
        pass

    @abstractmethod
    def getDatabaseType(self) -> DatabaseType:
        pass
