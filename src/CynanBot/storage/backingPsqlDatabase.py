import traceback
from asyncio import AbstractEventLoop
from typing import Optional

import asyncpg

from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.psqlCredentialsProvider import PsqlCredentialsProvider
from CynanBot.storage.psqlDatabaseConnection import PsqlDatabaseConnection
from CynanBot.timber.timberInterface import TimberInterface


class BackingPsqlDatabase(BackingDatabase):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        psqlCredentialsProvider: PsqlCredentialsProvider,
        timber: TimberInterface
    ):
        assert isinstance(eventLoop, AbstractEventLoop), f"malformed {eventLoop=}"
        assert isinstance(psqlCredentialsProvider, PsqlCredentialsProvider), f"malformed {psqlCredentialsProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__psqlCredentialsProvider: PsqlCredentialsProvider = psqlCredentialsProvider
        self.__timber: TimberInterface = timber

        self.__connectionPool: Optional[asyncpg.Pool] = None

    async def __createCollations(self, databaseConnection: DatabaseConnection):
        assert isinstance(databaseConnection, DatabaseConnection), f"malformed {databaseConnection=}"

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
