from typing import Final

from .gashaponRewardWatchStreakRepositoryInterface import GashaponRewardWatchStreakRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class GashaponRewardWatchStreakRepository(GashaponRewardWatchStreakRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> int | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT watchstreak FROM gashaponrewardwatchstreaks
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None
        else:
            return record[0]

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
                        CREATE TABLE IF NOT EXISTS gashaponrewardwatchstreaks (
                            watchstreak integer DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS gashaponrewardwatchstreaks (
                            watchstreak INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    ''',
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM gashaponrewardwatchstreaks
                WHERE chatteruserid = $1 AND twitchchannelid = $2
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('GashaponRewardWatchStreakRepository', f'Removed watch streak data ({chatterUserId=}) ({twitchChannelId=})')

    async def set(
        self,
        watchStreak: int | None,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        if watchStreak is not None and not utils.isValidInt(watchStreak):
            raise TypeError(f'watchStreak argument is malformed: \"{watchStreak}\"')
        elif watchStreak is not None and (watchStreak < 0 or watchStreak > utils.getIntMaxSafeSize()):
            raise ValueError(f'Streak argument is out of bounds: {watchStreak}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if watchStreak is None or watchStreak == 0:
            await self.remove(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )
            return

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO gashaponrewardwatchstreaks (chatteruserid, watchstreak, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET watchstreak = EXCLUDED.streak
            ''',
            chatterUserId, watchStreak, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('GashaponRewardWatchStreakRepository', f'Set watch streak data ({watchStreak=}) ({chatterUserId=}) ({twitchChannelId=})')
