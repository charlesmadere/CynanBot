from asyncio import AbstractEventLoop

import aiosqlite

from ..misc import utils as utils
from .backingDatabase import BackingDatabase
from .databaseConnection import DatabaseConnection
from .databaseType import DatabaseType
from .sqliteDatabaseConnection import SqliteDatabaseConnection


class BackingSqliteDatabase(BackingDatabase):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        backingDatabaseFile: str = 'database.sqlite'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not utils.isValidStr(backingDatabaseFile):
            raise TypeError(f'backingDatabaseFile argument is malformed: \"{backingDatabaseFile}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__backingDatabaseFile: str = backingDatabaseFile

    async def getConnection(self) -> DatabaseConnection:
        return SqliteDatabaseConnection(await aiosqlite.connect(
            database = self.__backingDatabaseFile,
            loop = self.__eventLoop
        ))

    def getDatabaseType(self) -> DatabaseType:
        return DatabaseType.SQLITE
