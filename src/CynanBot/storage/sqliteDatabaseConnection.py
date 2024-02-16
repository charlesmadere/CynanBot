from typing import Any, List, Optional

import aiosqlite

import CynanBot.misc.utils as utils
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.exceptions import DatabaseConnectionIsClosedException


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

    async def createTableIfNotExists(self, query: str, *args: Optional[Any]):
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        if utils.hasItems(args):
            await self.execute(query, args)
        else:
            await self.execute(query)

    async def execute(self, query: str, *args: Optional[Any]):
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()
        cursor = await self.__connection.execute(query, args)
        await self.__connection.commit()
        await cursor.close()

    async def fetchRow(self, query: str, *args: Optional[Any]) -> Optional[List[Any]]:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()
        cursor = await self.__connection.execute(query, args)
        row = await cursor.fetchone()

        if not utils.hasItems(row):
            await cursor.close()
            return None

        results: List[Any] = list()
        results.extend(row)

        await cursor.close()
        return results

    async def fetchRows(self, query: str, *args: Optional[Any]) -> Optional[List[List[Any]]]:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        self.__requireNotClosed()
        cursor = await self.__connection.execute(query, args)
        rows = await cursor.fetchall()

        if not utils.hasItems(rows):
            await cursor.close()
            return None

        records: List[List[Any]] = list()

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
