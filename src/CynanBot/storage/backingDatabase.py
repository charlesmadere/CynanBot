from abc import ABC, abstractmethod

from storage.databaseConnection import DatabaseConnection
from storage.databaseType import DatabaseType


class BackingDatabase(ABC):

    @abstractmethod
    async def getConnection(self) -> DatabaseConnection:
        pass

    @abstractmethod
    def getDatabaseType(self) -> DatabaseType:
        pass
