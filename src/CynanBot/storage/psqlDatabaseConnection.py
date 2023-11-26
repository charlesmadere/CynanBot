from typing import Any, List, Optional

import asyncpg
import misc.utils as utils
from storage.databaseConnection import DatabaseConnection
from storage.databaseType import DatabaseType
from storage.exceptions import DatabaseConnectionIsClosedException


class PsqlDatabaseConnection(DatabaseConnection):

    def __init__(self, connection: asyncpg.Connection, pool: asyncpg.Pool):
        if not isinstance(connection, asyncpg.Connection):
            raise ValueError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(pool, asyncpg.Pool):
            raise ValueError(f'pool argument is malformed: \"{pool}\"')

        self.__connection: asyncpg.Connection = connection
        self.__pool: asyncpg.Pool = pool

        self.__isClosed: bool = False

    async def close(self):
        if self.isClosed():
            return

        self.__isClosed = True
        await self.__pool.release(self.__connection)

    async def createTableIfNotExists(self, query: str, *args: Optional[Any]):
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        if utils.hasItems(args):
            await self.execute(query, args)
        else:
            await self.execute(query)

    async def execute(self, query: str, *args: Optional[Any]):
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        async with self.__connection.transaction():
            await self.__connection.execute(query, *args)

    async def fetchRow(self, query: str, *args: Optional[Any]) -> Optional[List[Any]]:
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()
        record = await self.__connection.fetchrow(query, *args)

        if not utils.hasItems(record):
            return None

        return list(record)

    async def fetchRows(self, query: str, *args: Optional[Any]) -> Optional[List[List[Any]]]:
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()
        records = await self.__connection.fetch(query, *args)

        if not utils.hasItems(records):
            return None

        rows: List[List[Any]] = list()

        for record in records:
            rows.append(list(record))

        return rows

    def getDatabaseType(self) -> DatabaseType:
        return DatabaseType.POSTGRESQL

    def isClosed(self) -> bool:
        return self.__isClosed

    def __requireNotClosed(self):
        if self.isClosed():
            raise DatabaseConnectionIsClosedException(f'This database connection has already been closed! ({self.getDatabaseType()})')
