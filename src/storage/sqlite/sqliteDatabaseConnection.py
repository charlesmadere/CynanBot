import sqlite3
from typing import Any, Final

import aiosqlite
from frozenlist import FrozenList

from ..databaseConnection import DatabaseConnection
from ..databaseType import DatabaseType
from ..exceptions import DatabaseConnectionIsClosedException, DatabaseOperationalError
from ...misc import utils as utils


class SqliteDatabaseConnection(DatabaseConnection):

    def __init__(self, connection: aiosqlite.Connection):
        if not isinstance(connection, aiosqlite.Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')

        self.__connection: Final[aiosqlite.Connection] = connection

        self.__isClosed: bool = False

    async def close(self):
        if self.isClosed:
            return

        self.__isClosed = True
        await self.__connection.close()

    @property
    def databaseType(self) -> DatabaseType:
        return DatabaseType.SQLITE

    async def execute(self, query: str, *args: Any | None):
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        cursor = await self.__connection.execute(query, args)
        await self.__connection.commit()
        await cursor.close()

    async def fetchRow(self, query: str, *args: Any | None) -> FrozenList[Any] | None:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        try:
            cursor = await self.__connection.execute(query, args)
        except sqlite3.OperationalError as e:
            raise DatabaseOperationalError(f'Encountered sqlite3 OperationalError when calling `fetchRow()`: {e}')

        row = await cursor.fetchone()

        if row is None or len(row) == 0:
            await cursor.close()
            return None

        frozenRow: FrozenList[Any] = FrozenList(row)
        frozenRow.freeze()

        await cursor.close()
        return frozenRow

    async def fetchRows(self, query: str, *args: Any | None) -> FrozenList[FrozenList[Any]] | None:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()

        try:
            cursor = await self.__connection.execute(query, args)
        except sqlite3.OperationalError as e:
            raise DatabaseOperationalError(f'Encountered sqlite3 OperationalError when calling `fetchRows()`: {e}')

        rows = await cursor.fetchall()

        if rows is None:
            await cursor.close()
            return None

        frozenResults: FrozenList[FrozenList[Any]] = FrozenList()

        for record in rows:
            frozenRow: FrozenList[Any] = FrozenList(record)
            frozenRow.freeze()

            frozenResults.append(frozenRow)

        frozenResults.freeze()
        await cursor.close()
        return frozenResults

    @property
    def isClosed(self) -> bool:
        return self.__isClosed

    def __requireNotClosed(self):
        if self.__isClosed:
            raise DatabaseConnectionIsClosedException(f'This database connection has already been closed! ({self.databaseType})')
