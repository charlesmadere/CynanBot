from datetime import datetime
from typing import Final

from .gashaponRewardHistoryRepositoryInterface import GashaponRewardHistoryRepositoryInterface
from ..models.gashaponRewardHistory import GashaponRewardHistory
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class GashaponRewardHistoryRepository(GashaponRewardHistoryRepositoryInterface):

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
        self.__cache: Final[dict[str, GashaponRewardHistory | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('GashaponRewardHistoryRepository', 'Caches cleared')

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getHistory(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> GashaponRewardHistory | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        rewardHistory = self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)
        if rewardHistory is not None:
            return rewardHistory

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT mostrecentreward FROM gashaponrewardhistory
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        if record is not None and len(record) >= 1:
            mostRecentReward = datetime.fromisoformat(record[0])

            rewardHistory = GashaponRewardHistory(
                mostRecentReward = mostRecentReward,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = rewardHistory
        return rewardHistory

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS gashaponrewardhistory (
                            chatteruserid text NOT NULL,
                            mostrecentreward text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS gashaponrewardhistory (
                            chatteruserid TEXT NOT NULL,
                            mostrecentreward TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def noteRewardGiven(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        mostRecentReward = datetime.now(self.__timeZoneRepository.getDefault())
        mostRecentRewardString = mostRecentReward.isoformat()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO gashaponrewardhistory (chatteruserid, mostrecentreward, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET mostrecentreward = EXCLUDED.mostrecentreward
            ''',
            chatterUserId, mostRecentRewardString, twitchChannelId,
        )

        await connection.close()

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = GashaponRewardHistory(
            mostRecentReward = mostRecentReward,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        self.__timber.log('GashaponRewardHistoryRepository', f'Updated gashapon reward history ({chatterUserId=}) ({mostRecentReward=}) ({twitchChannelId=})')
