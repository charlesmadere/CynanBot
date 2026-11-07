from datetime import datetime
from typing import Final

from lru import LRU

from .watchStreaksRepositoryInterface import WatchStreaksRepositoryInterface
from ..models.watchStreakStats import WatchStreakStats
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class WatchStreaksRepository(WatchStreaksRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 32,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 8 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, WatchStreakStats | None]] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('WatchStreaksRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if f'{twitchChannelId}:{chatterUserId}' in self.__cache:
            return self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT beststreak, currentstreak, mostrecentupdate FROM watchstreaks
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        stats: WatchStreakStats | None = None

        if record is not None and len(record) >= 1:
            stats = WatchStreakStats(
                mostRecentUpdate = datetime.fromisoformat(record[1]),
                bestStreak = record[0],
                currentStreak = record[2],
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = stats
        return stats

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
                        CREATE TABLE IF NOT EXISTS watchstreaks (
                            beststreak int DEFAULT 0 NOT NULL,
                            currentstreak int DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            mostrecentupdate text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS watchstreaks (
                            beststreak INTEGER NOT NULL DEFAULT 0,
                            currentstreak INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            mostrecentupdate TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    ''',
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def update(
        self,
        currentStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakStats:
        if not utils.isValidInt(currentStreak):
            raise TypeError(f'currentStreak argument is malformed: \"{currentStreak}\"')
        elif currentStreak < 0 or currentStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'currentStreak argument is out of bounds" {currentStreak}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentStats = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        now = self.__timeZoneRepository.getNow()

        if currentStats is None:
            currentStats = WatchStreakStats(
                mostRecentUpdate = now,
                bestStreak = currentStreak,
                currentStreak = currentStreak,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        bestStreak = int(max(currentStats.bestStreak, currentStreak))

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO watchstreaks (beststreak, currentstreak, chatteruserid, mostrecentupdate, twitchchannelid)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET beststreak = EXCLUDED.beststreak, currentstreak = EXCLUDED.currentstreak, mostrecentupdate = EXCLUDED.mostrecentupdate
            ''',
            bestStreak, currentStreak, chatterUserId, now.isoformat(), twitchChannelId,
        )

        await connection.close()

        newStats = WatchStreakStats(
            mostRecentUpdate = now,
            bestStreak = bestStreak,
            currentStreak = currentStreak,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = newStats
        self.__timber.log('WatchStreaksRepository', f'Updated stats ({bestStreak=}) ({currentStreak=}) ({chatterUserId=}) ({twitchChannelId=})')

        return newStats
