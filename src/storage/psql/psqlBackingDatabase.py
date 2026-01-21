import traceback
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Final

import asyncpg

from .psqlCredentialsProviderInterface import PsqlCredentialsProviderInterface
from .psqlDatabaseConnection import PsqlDatabaseConnection
from ..backingDatabase import BackingDatabase
from ..databaseConnection import DatabaseConnection
from ..databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class PsqlBackingDatabase(BackingDatabase):

    @dataclass(frozen = True, slots = True)
    class ConnectionPoolData:
        connectionPool: asyncpg.Pool
        wasConnectionPoolNewlyCreated: bool

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        psqlCredentialsProvider: PsqlCredentialsProviderInterface,
        timber: TimberInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(psqlCredentialsProvider, PsqlCredentialsProviderInterface):
            raise TypeError(f'psqlCredentialsProvider argument is malformed: \"{psqlCredentialsProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__psqlCredentialsProvider: Final[PsqlCredentialsProviderInterface] = psqlCredentialsProvider
        self.__timber: Final[TimberInterface] = timber

        self.__connectionPool: asyncpg.Pool | None = None

    async def __createCollations(self, databaseConnection: DatabaseConnection):
        if not isinstance(databaseConnection, DatabaseConnection):
            raise TypeError(f'databaseConnection argument is malformed: \"{databaseConnection}\"')

        await databaseConnection.execute('CREATE EXTENSION IF NOT EXISTS citext')

    @property
    def databaseType(self) -> DatabaseType:
        return DatabaseType.POSTGRESQL

    async def getConnection(self) -> DatabaseConnection:
        connectionPoolData = await self.__getConnectionPool()
        connection = await connectionPoolData.connectionPool.acquire()

        databaseConnection: DatabaseConnection = PsqlDatabaseConnection(
            connection = connection,
            pool = connectionPoolData.connectionPool,
        )

        if connectionPoolData.wasConnectionPoolNewlyCreated:
            await self.__createCollations(databaseConnection)

        return databaseConnection

    async def __getConnectionPool(self) -> ConnectionPoolData:
        wasConnectionPoolNewlyCreated = False
        connectionPool = self.__connectionPool

        if connectionPool is None:
            wasConnectionPoolNewlyCreated = True
            databaseName = await self.__psqlCredentialsProvider.requireDatabaseName()
            host = await self.__psqlCredentialsProvider.getHost()
            maxConnections = await self.__psqlCredentialsProvider.requireMaxConnections()
            password = await self.__psqlCredentialsProvider.getPassword()
            port = await self.__psqlCredentialsProvider.getPort()
            user = await self.__psqlCredentialsProvider.requireUser()

            connectionPool = await asyncpg.create_pool(
                database = databaseName,
                host = host,
                loop = self.__eventLoop,
                max_size = maxConnections,
                password = password,
                port = port,
                user = user,
            )

            if not isinstance(connectionPool, asyncpg.Pool):
                # this scenario should definitely be impossible, but the Python type checking was
                # getting angry without this check
                exception = RuntimeError(f'Failed to instantiate asyncpg.Pool ({connectionPool=}) ({databaseName=}) ({host=}) ({maxConnections=}) ({port=}) ({user=})')
                self.__timber.log('BackingPsqlDatabase', f'Failed to instantiate asyncpg.Pool ({connectionPool=}) ({databaseName=}) ({host=}) ({maxConnections=}) ({port=}) ({user=})', exception, traceback.format_exc())
                raise exception

            self.__connectionPool = connectionPool

        return PsqlBackingDatabase.ConnectionPoolData(
            connectionPool = connectionPool,
            wasConnectionPoolNewlyCreated = wasConnectionPoolNewlyCreated,
        )
