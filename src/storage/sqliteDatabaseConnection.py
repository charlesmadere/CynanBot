import sqlite3
from typing import Any

import aiosqlite

from .databaseConnection import DatabaseConnection
from .databaseType import DatabaseType
from .exceptions import (DatabaseConnectionIsClosedException,
                         DatabaseOperationalError)
from ..misc import utils as utils


class SqliteDatabaseConnection(DatabaseConnection):

    def __init__(self, connection: aiosqlite.Connection):
        if not isinstance(connection, aiosqlite.Connection):
            raise TypeError(f'connection argument is malformed: \"{connection}\"')

        self.__connection: aiosqlite.Connection = connection
        self.__isClosed: bool = False

    async def close(self):
        if self.__isClosed:
            return

        self.__isClosed = True
        await self.__connection.close()

    async def createTableIfNotExists(self, query: str, *args: Any | None):
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        if args is not None and len(args) >= 1:
            await self.execute(query, args)
        else:
            await self.execute(query)

    async def execute(self, query: str, *args: Any | None):
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()
        cursor = await self.__connection.execute(query, args)
        await self.__connection.commit()
        await cursor.close()

    async def fetchRow(self, query: str, *args: Any | None) -> list[Any] | None:
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

        results: list[Any] = list()
        results.extend(row)

        await cursor.close()
        return results

    async def fetchRows(self, query: str, *args: Any | None) -> list[list[Any]] | None:
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

        records: list[list[Any]] = list()

        for record in rows:
            records.append(list(record))

        await cursor.close()
        return records

    def getDatabaseType(self) -> DatabaseType:
        return DatabaseType.SQLITE

    def isClosed(self) -> bool:
        return self.__isClosed

    def __requireNotClosed(self):
        if self.__isClosed:
            raise DatabaseConnectionIsClosedException(f'This database connection has already been closed! ({self.getDatabaseType()})')
