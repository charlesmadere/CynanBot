from datetime import datetime, timezone
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import \
    ToxicTriviaOccurencesRepositoryInterface
from CynanBot.trivia.specialStatus.toxicTriviaResult import ToxicTriviaResult


class ToxicTriviaOccurencesRepository(ToxicTriviaOccurencesRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timeZone: timezone = timeZone

        self.__isDatabaseReady: bool = False

    async def fetchDetails(
        self,
        twitchChannel: str,
        userId: str
    ) -> ToxicTriviaResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT count, mostrecent FROM toxictriviaoccurences
                WHERE twitchchannel = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannel, userId
        )

        toxicCount: int = 0
        mostRecent: Optional[datetime] = None

        if utils.hasItems(record):
            toxicCount = record[0]
            mostRecent = utils.getDateTimeFromStr(record[1])

        await connection.close()

        return ToxicTriviaResult(
            mostRecent = mostRecent,
            newToxicCount = toxicCount,
            oldToxicCount = toxicCount,
            twitchChannel = twitchChannel,
            userId = userId
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def incrementToxicCount(
        self,
        twitchChannel: str,
        userId: str
    ) -> ToxicTriviaResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        result = await self.fetchDetails(
            twitchChannel = twitchChannel,
            userId = userId
        )

        newToxicCount: int = result.getOldToxicCount() + 1

        newResult = ToxicTriviaResult(
            mostRecent = datetime.now(self.__timeZone),
            newToxicCount = newToxicCount,
            oldToxicCount = result.getOldToxicCount(),
            twitchChannel = result.getTwitchChannel(),
            userId = result.getUserId()
        )

        await self.__updateToxicCount(
            newToxicCount = newResult.getNewToxicCount(),
            twitchChannel = newResult.getTwitchChannel(),
            userId = newResult.getUserId()
        )

        return newResult

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS toxictriviaoccurences (
                        count integer DEFAULT 0 NOT NULL,
                        mostrecent text NOT NULL,
                        twitchchannel public.citext NOT NULL,
                        userid public.citext NOT NULL,
                        PRIMARY KEY (twitchchannel, userid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS toxictriviaoccurences (
                        count INTEGER NOT NULL DEFAULT 0,
                        mostrecent TEXT NOT NULL,
                        twitchchannel TEXT NOT NULL COLLATE NOCASE,
                        userid TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (twitchchannel, userid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def __updateToxicCount(
        self,
        newToxicCount: int,
        twitchChannel: str,
        userId: str
    ):
        if not utils.isValidInt(newToxicCount):
            raise TypeError(f'newToxicCount argument is malformed: \"{newToxicCount}\"')
        if newToxicCount < 0 or newToxicCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newToxicCount argument is out of bounds: {newToxicCount}')
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        nowDateTime = datetime.now(self.__timeZone)
        nowDateTimeStr = nowDateTime.isoformat()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                    INSERT INTO toxictriviaoccurences (count, mostrecent, twitchchannel, userid)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (twitchchannel, userid) DO UPDATE SET count = EXCLUDED.count, mostrecent = EXCLUDED.mostrecent
            ''',
            newToxicCount, nowDateTimeStr, twitchChannel, userId
        )

        await connection.close()
