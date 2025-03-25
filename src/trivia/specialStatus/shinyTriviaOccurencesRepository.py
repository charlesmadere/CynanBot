from datetime import datetime

from .shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from .shinyTriviaResult import ShinyTriviaResult
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType


class ShinyTriviaOccurencesRepository(ShinyTriviaOccurencesRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZone argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

        self.__isDatabaseReady: bool = False

    async def fetchDetails(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> ShinyTriviaResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT count, mostrecent FROM shinytriviaoccurences
                WHERE twitchchannelid = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannelId, userId
        )

        shinyCount = 0
        mostRecent: datetime | None = None

        if record is not None and len(record) >= 1:
            shinyCount = record[0]
            mostRecent = datetime.fromisoformat(record[1])

        await connection.close()

        return ShinyTriviaResult(
            mostRecent = mostRecent,
            newShinyCount = shinyCount,
            oldShinyCount = shinyCount,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def incrementShinyCount(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> ShinyTriviaResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchDetails(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        newShinyCount = result.oldShinyCount + 1

        newResult = ShinyTriviaResult(
            mostRecent = datetime.now(self.__timeZoneRepository.getDefault()),
            newShinyCount = newShinyCount,
            oldShinyCount = result.oldShinyCount,
            twitchChannel = result.twitchChannel,
            twitchChannelId = result.twitchChannelId,
            userId = result.userId
        )

        await self.__updateShinyCount(
            newShinyCount = newResult.newShinyCount,
            twitchChannel = newResult.twitchChannel,
            twitchChannelId = newResult.twitchChannelId,
            userId = newResult.userId
        )

        return newResult

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS shinytriviaoccurences (
                            count integer DEFAULT 0 NOT NULL,
                            mostrecent text NOT NULL,
                            twitchchannelid text NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS shinytriviaoccurences (
                            count INTEGER NOT NULL DEFAULT 0,
                            mostrecent TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def __updateShinyCount(
        self,
        newShinyCount: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ):
        if not utils.isValidInt(newShinyCount):
            raise TypeError(f'newShinyCount argument is malformed: \"{newShinyCount}\"')
        elif newShinyCount < 0 or newShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newShinyCount argument is out of bounds: {newShinyCount}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO shinytriviaoccurences (count, mostrecent, twitchchannelid, userid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (twitchchannelid, userid) DO UPDATE SET count = EXCLUDED.count, mostrecent = EXCLUDED.mostrecent
            ''',
            newShinyCount, nowDateTime.isoformat(), twitchChannelId, userId
        )

        await connection.close()
