from lru import LRU

from .asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from ..models.asplodieStats import AsplodieStats
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class AsplodieStatsRepository(AsplodieStatsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        cacheSize: int = 64
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > 256:
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__cache: LRU[str, AsplodieStats | None] = LRU(cacheSize)

    async def addAsplodie(
        self,
        durationAsplodiedSeconds: int,
        chatterUserId: str,
        twitchChannelId: str
    ) -> AsplodieStats:
        raise RuntimeError()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('AsplodieStatsRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> AsplodieStats:
        raise RuntimeError()

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS asplodiestats (
                            totalasplodies int DEFAULT 0 NOT NULL,
                            totaldurationasplodiedseconds bigint DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS asplodiestats (
                            totalasplodies INTEGER NOT NULL DEFAULT 0,
                            totaldurationasplodiedseconds INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
