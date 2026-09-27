from typing import Final

from frozenlist import FrozenList

from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessDate import CutenessDate
from .cutenessHistoryEntry import CutenessHistoryEntry
from .cutenessHistoryResult import CutenessHistoryResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult
from .cutenessLeaderboardResult import CutenessLeaderboardResult
from .cutenessRepositoryInterface import CutenessRepositoryInterface
from .cutenessResult import CutenessResult
from .incrementedCutenessResult import IncrementedCutenessResult
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType


class CutenessRepository(CutenessRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        historyLeaderboardSize: int = 3,
        historySize: int = 5,
        leaderboardSize: int = 10,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not utils.isValidInt(historyLeaderboardSize):
            raise TypeError(f'historyLeaderboardSize argument is malformed: \"{historyLeaderboardSize}\"')
        elif historyLeaderboardSize < 2 or historyLeaderboardSize > 6:
            raise ValueError(f'historyLeaderboardSize argument is out of bounds: {historyLeaderboardSize}')
        elif not utils.isValidInt(historySize):
            raise TypeError(f'historySize argument is malformed: \"{historySize}\"')
        elif historySize < 3 or historySize > 12:
            raise ValueError(f'historySize argument is out of bounds: {historySize}')
        elif not utils.isValidInt(leaderboardSize):
            raise TypeError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 3 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: {leaderboardSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__historyLeaderboardSize: Final[int] = historyLeaderboardSize
        self.__historySize: Final[int] = historySize
        self.__leaderboardSize: Final[int] = leaderboardSize

        self.__isDatabaseReady: bool = False

    async def fetchCuteness(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> CutenessResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        cutenessDate = CutenessDate()

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT cuteness, userid FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND utcyearandmonth = $3
                LIMIT 1
            ''',
            twitchChannelId, userId, cutenessDate.getDatabaseString(),
        )

        await connection.close()

        if record is None or len(record) == 0:
            return CutenessResult(
                cutenessDate = cutenessDate,
                cuteness = 0,
                userId = userId,
            )
        else:
            return CutenessResult(
                cutenessDate = cutenessDate,
                cuteness = record[0],
                userId = userId,
            )

    async def fetchCutenessChampions(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> CutenessChampionsResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT userid, SUM(cuteness) AS totalcuteness FROM cuteness
                WHERE twitchchannelid = $1 AND userid != $2
                GROUP BY userid
                ORDER BY totalcuteness DESC
                LIMIT $3
            ''',
            twitchChannelId, twitchChannelId, self.__leaderboardSize,
        )

        await connection.close()

        if records is None or len(records) == 0:
            return CutenessChampionsResult(
                champions = None,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
            )

        champions: FrozenList[CutenessLeaderboardEntry] = FrozenList()

        for index, record in enumerate(records):
            # Cuteness can potentially arrive from the database as a decimal.Decimal type,
            # so let's make sure to convert that into an int.
            cuteness = int(round(record[1]))

            champions.append(CutenessLeaderboardEntry(
                cuteness = cuteness,
                rank = index + 1,
                userId = record[0],
            ))

        champions.freeze()

        return CutenessChampionsResult(
            champions = champions,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessHistory(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> CutenessHistoryResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cuteness, utcyearandmonth FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND cuteness IS NOT NULL AND cuteness >= 1
                ORDER BY utcyearandmonth DESC
                LIMIT $3
            ''',
            twitchChannelId, userId, self.__historySize,
        )

        if records is None or len(records) == 0:
            await connection.close()
            return CutenessHistoryResult(
                userId = userId,
            )

        entries: list[CutenessHistoryEntry] = list()

        for record in records:
            entries.append(CutenessHistoryEntry(
                cutenessDate = CutenessDate(record[1]),
                cuteness = record[0],
                userId = userId,
            ))

        # sort entries into newest to oldest order
        entries.sort(key = lambda entry: entry.cutenessDate, reverse = True)

        frozenEntries: FrozenList[CutenessHistoryEntry] = FrozenList(entries)
        frozenEntries.freeze()

        record = await connection.fetchRow(
            '''
                SELECT SUM(cuteness) FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND cuteness IS NOT NULL AND cuteness >= 1
                LIMIT 1
            ''',
            twitchChannelId, userId,
        )

        totalCuteness = 0

        if record is not None and len(record) >= 1:
            # this should be impossible at this point, but let's just be safe
            totalCuteness = int(round(record[0]))

        record = await connection.fetchRow(
            '''
                SELECT cuteness, utcyearandmonth FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND cuteness IS NOT NULL AND cuteness >= 1
                ORDER BY cuteness DESC
                LIMIT 1
            ''',
            twitchChannelId, userId,
        )

        bestCuteness: CutenessHistoryEntry | None = None

        if record is not None and len(record) >= 1:
            # again, this should be impossible here, but let's just be safe
            bestCuteness = CutenessHistoryEntry(
                cutenessDate = CutenessDate(record[1]),
                cuteness = record[0],
                userId = userId,
            )

        await connection.close()

        return CutenessHistoryResult(
            userId = userId,
            bestCuteness = bestCuteness,
            entries = frozenEntries,
            totalCuteness = totalCuteness,
        )

    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> IncrementedCutenessResult:
        if not utils.isValidInt(incrementAmount):
            raise TypeError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount < utils.getLongMinSafeSize() or incrementAmount > utils.getLongMaxSafeSize():
            raise ValueError(f'incrementAmount argument is out of bounds: {incrementAmount}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        cutenessDate = CutenessDate()

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND utcyearandmonth = $3
                LIMIT 1
            ''',
            twitchChannelId, userId, cutenessDate.getDatabaseString(),
        )

        previousCuteness = 0

        if record is not None and len(record) >= 1:
            previousCuteness = record[0]

        newCuteness = previousCuteness + incrementAmount

        if newCuteness < 0:
            newCuteness = 0
        elif newCuteness > utils.getLongMaxSafeSize():
            raise OverflowError(f'New cuteness would be too large ({newCuteness=}) ({previousCuteness=}) ({incrementAmount=})')

        await connection.execute(
            '''
                INSERT INTO cuteness (cuteness, twitchchannelid, userid, utcyearandmonth)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (twitchchannelid, userid, utcyearandmonth) DO UPDATE SET cuteness = EXCLUDED.cuteness
            ''',
            newCuteness, twitchChannelId, userId, cutenessDate.getDatabaseString(),
        )

        await connection.close()

        return IncrementedCutenessResult(
            cutenessDate = cutenessDate,
            newCuteness = newCuteness,
            previousCuteness = previousCuteness,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

    async def fetchCutenessLeaderboard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        specificLookupUserId: str | None = None,
    ) -> CutenessLeaderboardResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif specificLookupUserId is not None and not isinstance(specificLookupUserId, str):
            raise TypeError(f'specificLookupUserId argument is malformed: \"{specificLookupUserId}\"')

        cutenessDate = CutenessDate()

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cuteness, userid FROM cuteness
                WHERE twitchchannelid = $1 AND utcyearandmonth = $2 AND cuteness IS NOT NULL AND cuteness >= 1 AND userid != $3
                ORDER BY cuteness DESC
                LIMIT $4
            ''',
            twitchChannelId, cutenessDate.getDatabaseString(), twitchChannelId, self.__leaderboardSize,
        )

        await connection.close()

        if records is None or len(records) == 0:
            return CutenessLeaderboardResult(
                cutenessDate = cutenessDate,
            )

        entries: FrozenList[CutenessLeaderboardEntry] = FrozenList()

        for index, record in enumerate(records):
            entries.append(CutenessLeaderboardEntry(
                cuteness = record[0],
                rank = index + 1,
                userId = record[1],
            ))

        entries.freeze()

        specificLookupAlreadyInResults = False
        if utils.isValidStr(specificLookupUserId):
            for entry in entries:
                if entry.userId == specificLookupUserId:
                    specificLookupAlreadyInResults = True
                    break

        specificLookupCutenessResult: CutenessResult | None = None
        if not specificLookupAlreadyInResults and utils.isValidStr(specificLookupUserId):
            specificLookupCutenessResult = await self.fetchCuteness(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
                userId = specificLookupUserId,
            )

        return CutenessLeaderboardResult(
            cutenessDate = cutenessDate,
            specificLookupCutenessResult = specificLookupCutenessResult,
            entries = entries,
        )

    async def fetchCutenessLeaderboardHistory(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> CutenessLeaderboardHistoryResult:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT DISTINCT utcyearandmonth FROM cuteness
                WHERE twitchchannelid = $1 AND utcyearandmonth != $2
                ORDER BY utcyearandmonth DESC
                LIMIT $3
            ''',
            twitchChannelId, CutenessDate().getDatabaseString(), self.__historyLeaderboardSize,
        )

        if records is None or len(records) == 0:
            await connection.close()
            return CutenessLeaderboardHistoryResult(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId,
            )

        leaderboards: FrozenList[CutenessLeaderboardResult] = FrozenList()

        for record in records:
            cutenessDate = CutenessDate(record[0])
            monthRecords = await connection.fetchRows(
                '''
                    SELECT cuteness, userid FROM cuteness
                    WHERE cuteness IS NOT NULL AND cuteness >= 1 AND twitchchannelid = $1 AND userid != $2 AND utcyearandmonth = $3
                    ORDER BY cuteness DESC
                    LIMIT $4
                ''',
                twitchChannelId, twitchChannelId, cutenessDate.getDatabaseString(), self.__historyLeaderboardSize,
            )

            if monthRecords is None or len(monthRecords) == 0:
                continue

            entries: FrozenList[CutenessLeaderboardEntry] = FrozenList()
            rank = 1

            for monthRecord in monthRecords:
                entries.append(CutenessLeaderboardEntry(
                    cuteness = monthRecord[0],
                    rank = rank,
                    userId = monthRecord[1],
                ))
                rank = rank + 1

            entries.freeze()

            leaderboards.append(CutenessLeaderboardResult(
                cutenessDate = cutenessDate,
                entries = entries,
            ))

        leaderboards.freeze()
        await connection.close()

        return CutenessLeaderboardHistoryResult(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            leaderboards = leaderboards,
        )

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
                        CREATE TABLE IF NOT EXISTS cuteness (
                            cuteness bigint DEFAULT 0 NOT NULL,
                            twitchchannelid text NOT NULL,
                            userid text NOT NULL,
                            utcyearandmonth text NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid, utcyearandmonth)
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS cuteness (
                            cuteness INTEGER NOT NULL DEFAULT 0,
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            utcyearandmonth TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid, utcyearandmonth)
                        ) STRICT
                    ''',
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
