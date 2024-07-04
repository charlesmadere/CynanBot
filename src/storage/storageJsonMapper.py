from typing import Any

from .databaseType import DatabaseType
from .storageJsonMapperInterface import StorageJsonMapperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class StorageJsonMapper(StorageJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    def parseDatabaseType(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType | None:
        if not utils.isValidStr(databaseType):
            return None

        databaseType = databaseType.lower()

        match databaseType:
            case 'postgres': return DatabaseType.POSTGRESQL
            case 'postgresql': return DatabaseType.POSTGRESQL
            case 'sqlite': return DatabaseType.SQLITE
            case _:
                self.__timber.log('StorageJsonMapper', f'Encountered unknown DatabaseType value: \"{databaseType}\"')
                return None

    async def parseDatabaseTypeAsync(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType | None:
        return self.parseDatabaseType(databaseType)

    def requireDatabaseType(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        result = self.parseDatabaseType(databaseType)

        if result is None:
            raise ValueError(f'Unable to parse \"{databaseType}\" into DatabaseType value!')

        return result

    async def requireDatabaseTypeAsync(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        result = await self.parseDatabaseTypeAsync(databaseType)

        if result is None:
            raise ValueError(f'Unable to parse \"{databaseType}\" into DatabaseType value!')

        return result
