from abc import ABC, abstractmethod

from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType


class BackingDatabase(ABC):

    @abstractmethod
    async def getConnection(self) -> DatabaseConnection:
        pass

    @abstractmethod
    def getDatabaseType(self) -> DatabaseType:
        pass
