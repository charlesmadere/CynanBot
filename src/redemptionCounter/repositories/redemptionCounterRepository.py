from typing import Final

from lru import LRU

from .redemptionCounterRepositoryInterface import RedemptionCounterRepositoryInterface
from ..models.redemptionCount import RedemptionCount
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class RedemptionCounterRepository(RedemptionCounterRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        cacheSize: int = 32,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, RedemptionCount | None]] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('RedemptionCounterRepository', 'Caches cleared')

    async def __fetchFromDatabase(
        self,
        connection: DatabaseConnection,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str,
    ) -> RedemptionCount:
        record = await connection.fetchRow(
            '''
                SELECT count FROM redemptioncounter
                WHERE chatteruserid = $1 AND countername = $2 AND twitchchannelid = $3
                LIMIT 1
            ''',
            chatterUserId, counterName, twitchChannelId,
        )

        redemptionCount: RedemptionCount

        if record is None or len(record) == 0:
            redemptionCount = RedemptionCount(
                count = 0,
                chatterUserId = chatterUserId,
                counterName = counterName,
                twitchChannelId = twitchChannelId,
            )
        else:
            redemptionCount = RedemptionCount(
                count = record[0],
                chatterUserId = chatterUserId,
                counterName = counterName,
                twitchChannelId = twitchChannelId,
            )

        return redemptionCount

    async def get(
        self,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str,
    ) -> RedemptionCount:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(counterName):
            raise TypeError(f'counterName argument is malformed: \"{counterName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        redemptionCount = self.__cache.get(f'{twitchChannelId}:{counterName}:{chatterUserId}', None)

        if redemptionCount is not None:
            return redemptionCount

        connection = await self.__getDatabaseConnection()

        redemptionCount = await self.__fetchFromDatabase(
            connection = connection,
            chatterUserId = chatterUserId,
            counterName = counterName,
            twitchChannelId = twitchChannelId,
        )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{counterName}:{chatterUserId}'] = redemptionCount

        return redemptionCount

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def increment(
        self,
        incrementAmount: int,
        chatterUserId: str,
        counterName: str,
        twitchChannelId: str,
    ) -> RedemptionCount:
        if not utils.isValidInt(incrementAmount):
            raise TypeError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount < 1 or incrementAmount > utils.getShortMaxSafeSize():
            raise ValueError(f'incrementAmount argument is out of bounds: {incrementAmount}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(counterName):
            raise TypeError(f'counterName argument is malformed: \"{counterName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()

        redemptionCount = await self.__fetchFromDatabase(
            connection = connection,
            chatterUserId = chatterUserId,
            counterName = counterName,
            twitchChannelId = twitchChannelId,
        )

        newRedemptionCount = RedemptionCount(
            count = redemptionCount.count + incrementAmount,
            chatterUserId = chatterUserId,
            counterName = counterName,
            twitchChannelId = twitchChannelId,
        )

        await connection.execute(
            '''
                INSERT INTO redemptioncounter (count, chatteruserid, countername, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (chatteruserid, countername, twitchchannelid) DO UPDATE SET count = EXCLUDED.count
            ''',
            newRedemptionCount.count, chatterUserId, counterName, twitchChannelId,
        )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{counterName}:{chatterUserId}'] = newRedemptionCount
        self.__timber.log('RedemptionCounterRepository', f'Incremented {counterName} from {redemptionCount.count} to {newRedemptionCount.count} for {chatterUserId} in {twitchChannelId}')

        return newRedemptionCount

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS redemptioncounter (
                            count bigint DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            countername text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, countername, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS redemptioncounter (
                            count INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            countername TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, countername, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
