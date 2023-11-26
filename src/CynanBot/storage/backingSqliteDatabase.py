from asyncio import AbstractEventLoop

import aiosqlite

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.sqliteDatabaseConnection import SqliteDatabaseConnection


class BackingSqliteDatabase(BackingDatabase):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        backingDatabaseFile: str = 'CynanBotCommon/storage/database.sqlite'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not utils.isValidStr(backingDatabaseFile):
            raise ValueError(f'backingDatabaseFile argument is malformed: \"{backingDatabaseFile}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__backingDatabaseFile: str = backingDatabaseFile

    async def getConnection(self) -> DatabaseConnection:
        return SqliteDatabaseConnection(await aiosqlite.connect(
            database = self.__backingDatabaseFile,
            loop = self.__eventLoop
        ))

    def getDatabaseType(self) -> DatabaseType:
        return DatabaseType.SQLITE
