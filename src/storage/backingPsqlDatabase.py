import traceback
from asyncio import AbstractEventLoop

import asyncpg

from .backingDatabase import BackingDatabase
from .databaseConnection import DatabaseConnection
from .databaseType import DatabaseType
from .psqlCredentialsProvider import PsqlCredentialsProvider
from .psqlDatabaseConnection import PsqlDatabaseConnection
from ..timber.timberInterface import TimberInterface


class BackingPsqlDatabase(BackingDatabase):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        psqlCredentialsProvider: PsqlCredentialsProvider,
        timber: TimberInterface
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(psqlCredentialsProvider, PsqlCredentialsProvider):
            raise TypeError(f'psqlCredentialsProvider argument is malformed: \"{psqlCredentialsProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__psqlCredentialsProvider: PsqlCredentialsProvider = psqlCredentialsProvider
        self.__timber: TimberInterface = timber

        self.__connectionPool: asyncpg.Pool | None = None

    async def __createCollations(self, databaseConnection: DatabaseConnection):
        if not isinstance(databaseConnection, DatabaseConnection):
            raise TypeError(f'databaseConnection argument is malformed: \"{databaseConnection}\"')

        await databaseConnection.execute('CREATE EXTENSION IF NOT EXISTS citext')

    async def getConnection(self) -> DatabaseConnection:
        connectionPoolCreated = False
        connectionPool = self.__connectionPool

        if connectionPool is None:
            connectionPoolCreated = True
            databaseName = await self.__psqlCredentialsProvider.requireDatabaseName()
            maxConnections = await self.__psqlCredentialsProvider.requireMaxConnections()
            password = await self.__psqlCredentialsProvider.getPassword()
            user = await self.__psqlCredentialsProvider.requireUser()

            connectionPool = await asyncpg.create_pool(
                database = databaseName,
                loop = self.__eventLoop,
                max_size = maxConnections,
                password = password,
                user = user
            )

            self.__connectionPool = connectionPool

        if not isinstance(connectionPool, asyncpg.Pool):
            # this scenario should definitely be impossible, but the Python type checking was
            # getting angry without this check
            exception = RuntimeError(f'Failed to instantiate asyncpg.Pool: \"{connectionPool}\"')
            self.__timber.log('BackingPsqlDatabase', f'Failed to instantiate asyncpg.Pool: \"{connectionPool}\" ({exception=})', exception, traceback.format_exc())
            raise exception

        connection = await connectionPool.acquire()

        databaseConnection: DatabaseConnection = PsqlDatabaseConnection(
            connection = connection,
            pool = connectionPool
        )

        if connectionPoolCreated:
            await self.__createCollations(databaseConnection)

        return databaseConnection

    def getDatabaseType(self) -> DatabaseType:
        return DatabaseType.POSTGRESQL
