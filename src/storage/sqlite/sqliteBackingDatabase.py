from asyncio import AbstractEventLoop
from typing import Final

import aiosqlite

from .sqliteDatabaseConnection import SqliteDatabaseConnection
from ..backingDatabase import BackingDatabase
from ..databaseConnection import DatabaseConnection
from ..databaseType import DatabaseType
from ...misc import utils as utils


class SqliteBackingDatabase(BackingDatabase):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        backingDatabaseFile: str = '../db/database.sqlite',
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not utils.isValidStr(backingDatabaseFile):
            raise TypeError(f'backingDatabaseFile argument is malformed: \"{backingDatabaseFile}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__backingDatabaseFile: Final[str] = backingDatabaseFile

    @property
    def databaseType(self) -> DatabaseType:
        return DatabaseType.SQLITE

    async def getConnection(self) -> DatabaseConnection:
        return SqliteDatabaseConnection(await aiosqlite.connect(
            database = self.__backingDatabaseFile,
            loop = self.__eventLoop,
        ))
