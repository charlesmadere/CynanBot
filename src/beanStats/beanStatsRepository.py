from datetime import datetime

from .beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from .chatterBeanStats import ChatterBeanStats
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class BeanStatsRepository(BeanStatsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False

    async def getStats(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        await self.__userIdsRepository.setUser(
            userId = chatterUserId,
            userName = chatterUserName
        )

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT fails, successes, mostrecentfail, mostrecentsuccess FROM beanstats
                WHERE userid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        mostRecentFail: datetime | None = None
        if utils.isValidStr(record[2]):
            mostRecentFail = datetime.fromisoformat(record[2])

        mostRecentSuccess: datetime | None = None
        if utils.isValidStr(record[3]):
            mostRecentSuccess = datetime.fromisoformat(record[3])

        return ChatterBeanStats(
            mostRecentFail = mostRecentFail,
            mostRecentSuccess = mostRecentSuccess,
            failedBeanAttempts = record[0],
            successfulBeans = record[1],
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def incrementFails(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        beanStats = await self.getStats(
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        mostRecentFail = datetime.now(self.__timeZoneRepository.getDefault())

        mostRecentSuccess: datetime | None = None
        if beanStats is not None:
            mostRecentSuccess = beanStats.mostRecentSuccess

        failedBeanAttempts: int
        if beanStats is None:
            failedBeanAttempts = 1
        else:
            failedBeanAttempts = beanStats.failedBeanAttempts + 1

        successfulBeans: int
        if beanStats is None:
            successfulBeans = 0
        else:
            successfulBeans = beanStats.successfulBeans

        newBeanStats = ChatterBeanStats(
            mostRecentFail = mostRecentFail,
            mostRecentSuccess = mostRecentSuccess,
            failedBeanAttempts = failedBeanAttempts,
            successfulBeans = successfulBeans,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        await self.__saveStatsToDatabase(newBeanStats)
        return newBeanStats

    async def incrementSuccesses(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> ChatterBeanStats:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        beanStats = await self.getStats(
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        mostRecentFail: datetime | None = None
        if beanStats is not None:
            mostRecentFail = beanStats.mostRecentFail

        mostRecentSuccess = datetime.now(self.__timeZoneRepository.getDefault())

        failedBeanAttempts: int
        if beanStats is None:
            failedBeanAttempts = 0
        else:
            failedBeanAttempts = beanStats.failedBeanAttempts

        successfulBeans: int
        if beanStats is None:
            successfulBeans = 1
        else:
            successfulBeans = beanStats.successfulBeans + 1

        newBeanStats = ChatterBeanStats(
            mostRecentFail = mostRecentFail,
            mostRecentSuccess = mostRecentSuccess,
            failedBeanAttempts = failedBeanAttempts,
            successfulBeans = successfulBeans,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        await self.__saveStatsToDatabase(newBeanStats)
        return newBeanStats

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS beanstats (
                            fails int DEFAULT 0 NOT NULL,
                            successes int DEFAULT 0 NOT NULL,
                            mostrecentfail text DEFAULT NULL,
                            mostrecentsuccess text DEFAULT NULL,
                            twitchchannelid text NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS beanstats (
                            fails INTEGER NOT NULL DEFAULT 0,
                            successes INTEGER NOT NULL DEFAULT 0,
                            mostrecentfail TEXT DEFAULT NULL,
                            mostrecentsuccess TEXT DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def __saveStatsToDatabase(self, stats: ChatterBeanStats):
        if not isinstance(stats, ChatterBeanStats):
            raise TypeError(f'stats argument is malformed: \"{stats}\"')

        mostRecentFailString: str | None = None
        if stats.mostRecentFail is not None:
            mostRecentFailString = stats.mostRecentFail.isoformat()

        mostRecentSuccessString: str | None = None
        if stats.mostRecentSuccess is not None:
            mostRecentSuccessString = stats.mostRecentSuccess.isoformat()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO beanstats (fails, successes, mostrecentfail, mostrecentsuccess, twitchchannelid, userid)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (twitchchannelid, userid) DO UPDATE SET fails = EXCLUDED.fails, successes = EXCLUDED.successes, mostrecentfail = EXCLUDED.mostrecentfail, mostrecentsuccess = EXCLUDED.mostrecentsuccess
            ''',
            stats.failedBeanAttempts, stats.successfulBeans, mostRecentFailString, mostRecentSuccessString, stats.twitchChannelId, stats.chatterUserId
        )

        await connection.close()
