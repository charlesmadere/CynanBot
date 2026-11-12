from datetime import datetime
from typing import Final

from .watchStreakRewardHistoryRepositoryInterface import WatchStreakRewardHistoryRepositoryInterface
from ..models.watchStreakRewardHistoryData import WatchStreakRewardHistoryData
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class WatchStreakRewardHistoryRepository(WatchStreakRewardHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> WatchStreakRewardHistoryData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT watchstreak, mostrecentreward FROM watchstreakrewardhistory
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        data: WatchStreakRewardHistoryData | None = None

        if record is not None and len(record) >= 1:
            data = WatchStreakRewardHistoryData(
                mostRecentReward = datetime.fromisoformat(record[1]),
                watchStreak = record[0],
            )

        return data

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
                        CREATE TABLE IF NOT EXISTS watchstreakrewardhistory (
                            watchstreak integer DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            mostrecentreward text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS watchstreakrewardhistory (
                            watchstreak INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            mostrecentreward TEXT NOT NULL,
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
        watchStreak: int,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        if not utils.isValidInt(watchStreak):
            raise TypeError(f'watchStreak argument is malformed: \"{watchStreak}\"')
        elif watchStreak < 0 or watchStreak > utils.getIntMaxSafeSize():
            raise ValueError(f'watchStreak argument is out of bounds: \"{watchStreak}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = self.__timeZoneRepository.getNow()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO watchstreakrewardhistory (watchstreak, chatteruserid, mostrecentreward, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET watchstreak = EXCLUDED.watchstreak, mostrecentreward = EXCLUDED.mostrecentreward
            ''',
            watchStreak, chatterUserId, now.isoformat(), twitchChannelId,
        )

        await connection.close()
        self.__timber.log('WatchStreakRewardHistoryRepository', f'Updated data ({watchStreak=}) ({chatterUserId=}) ({twitchChannelId=})')
