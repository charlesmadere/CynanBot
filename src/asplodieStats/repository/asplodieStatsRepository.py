from typing import Final

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
        cacheSize: int = 64,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > 256:
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, AsplodieStats | None]] = LRU(cacheSize)

    async def addAsplodie(
        self,
        isSelfAsplodie: bool,
        durationAsplodiedSeconds: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AsplodieStats:
        if not utils.isValidBool(isSelfAsplodie):
            raise TypeError(f'isSelfAsplodie argument is malformed: \"{isSelfAsplodie}\"')
        elif not utils.isValidInt(durationAsplodiedSeconds):
            raise TypeError(f'durationAsplodiedSeconds argument is malformed: \"{durationAsplodiedSeconds}\"')
        elif durationAsplodiedSeconds < 1 or durationAsplodiedSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationAsplodiedSeconds argument is out of bounds: {durationAsplodiedSeconds}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        oldAsplodieStats = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        newSelfAsplodies = oldAsplodieStats.selfAsplodies
        if isSelfAsplodie: newSelfAsplodies += 1

        newTotalAsplodies = oldAsplodieStats.totalAsplodies + 1
        newTotalDurationAsplodiedSeconds = oldAsplodieStats.totalDurationAsplodiedSeconds + durationAsplodiedSeconds

        newAsplodieStats = AsplodieStats(
            selfAsplodies = newSelfAsplodies,
            totalAsplodies = newTotalAsplodies,
            totalDurationAsplodiedSeconds = newTotalDurationAsplodiedSeconds,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO asplodiestats (selfasplodies, totalasplodies, totaldurationasplodiedseconds, chatteruserid, twitchchannelid)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET selfasplodies = EXCLUDED.selfasplodies, totalasplodies = EXCLUDED.totalasplodies, totaldurationasplodiedseconds = EXCLUDED.totaldurationasplodiedseconds
            ''',
            newSelfAsplodies, newTotalAsplodies, newTotalDurationAsplodiedSeconds, chatterUserId, twitchChannelId
        )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = newAsplodieStats
        self.__timber.log('AsplodieStatsRepository', f'Updated asplodie stats ({newAsplodieStats=})')

        return newAsplodieStats

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('AsplodieStatsRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> AsplodieStats:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        result = self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)

        if result is not None:
            return result

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT selfasplodies, totalasplodies, totaldurationasplodiedseconds FROM asplodiestats
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        if record is None or len(record) == 0:
            result = AsplodieStats(
                selfAsplodies = 0,
                totalAsplodies = 0,
                totalDurationAsplodiedSeconds = 0,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )
        else:
            result = AsplodieStats(
                selfAsplodies = record[0],
                totalAsplodies = record[1],
                totalDurationAsplodiedSeconds = record[2],
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = result
        return result

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
                            selfasplodies int DEFAULT 0 NOT NULL,
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
                            selfasplodies INTEGER NOT NULL DEFAULT 0,
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
