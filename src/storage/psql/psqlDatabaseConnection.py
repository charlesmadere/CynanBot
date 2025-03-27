from typing import Any, Final

import asyncpg
from frozenlist import FrozenList

from ..databaseConnection import DatabaseConnection
from ..databaseType import DatabaseType
from ..exceptions import DatabaseConnectionIsClosedException
from ...misc import utils as utils


class PsqlDatabaseConnection(DatabaseConnection):

    def __init__(self, connection: asyncpg.Connection, pool: asyncpg.Pool):
        if not isinstance(connection, asyncpg.Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')
        elif not isinstance(pool, asyncpg.Pool):
            raise TypeError(f'pool argument is malformed: \"{pool}\"')

        self.__connection: Final[asyncpg.Connection] = connection
        self.__pool: Final[asyncpg.Pool] = pool

        self.__isClosed: bool = False

    async def close(self):
        if self.isClosed:
            return

        self.__isClosed = True
        await self.__pool.release(self.__connection)

    @property
    def databaseType(self) -> DatabaseType:
        return DatabaseType.POSTGRESQL

    async def execute(self, query: str, *args: Any | None):
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        async with self.__connection.transaction():
            await self.__connection.execute(query, *args)

    async def fetchRow(self, query: str, *args: Any | None) -> FrozenList[Any] | None:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        record = await self.__connection.fetchrow(query, *args)

        if record is None or len(record) == 0:
            return None

        frozenRecord: FrozenList[Any] = FrozenList(record)
        frozenRecord.freeze()

        return frozenRecord

    async def fetchRows(self, query: str, *args: Any | None) -> FrozenList[FrozenList[Any]] | None:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        records = await self.__connection.fetch(query, *args)

        if records is None or len(records) == 0:
            return None

        frozenRows: FrozenList[FrozenList[Any]] = FrozenList()

        for record in records:
            frozenRecord: FrozenList[Any] = FrozenList(record)
            frozenRecord.freeze()

            frozenRows.append(frozenRecord)

        frozenRows.freeze()
        return frozenRows

    @property
    def isClosed(self) -> bool:
        return self.__isClosed

    def __requireNotClosed(self):
        if self.isClosed:
            raise DatabaseConnectionIsClosedException(f'This database connection has already been closed! ({self.databaseType})')
