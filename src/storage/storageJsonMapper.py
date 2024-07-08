from typing import Any

from .databaseType import DatabaseType
from .storageJsonMapperInterface import StorageJsonMapperInterface


class StorageJsonMapper(StorageJsonMapperInterface):

    def parseDatabaseType(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        if not isinstance(databaseType, str):
            raise TypeError(f'databaseType argument is malformed: \"{databaseType}\"')

        databaseType = databaseType.lower()

        match databaseType:
            case 'postgresql': return DatabaseType.POSTGRESQL
            case 'sqlite': return DatabaseType.SQLITE
            case _: raise ValueError(f'Unknown DatabaseType value: \"{databaseType}\"')

    async def parseDatabaseTypeAsync(
        self,
        databaseType: str | Any | None
    ) -> DatabaseType:
        return self.parseDatabaseType(databaseType)
