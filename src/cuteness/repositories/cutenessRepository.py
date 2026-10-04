from datetime import datetime
from typing import Final

from frozenlist import FrozenList

from .cutenessRepositoryInterface import CutenessRepositoryInterface
from ..mappers.cutenessMapperInterface import CutenessMapperInterface
from ..models.cutenessChampionsResult import CutenessChampionsResult
from ..models.cutenessHistoryEntry import CutenessHistoryEntry
from ..models.cutenessHistoryResult import CutenessHistoryResult
from ..models.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from ..models.cutenessLeaderboardHistoryResult import CutenessLeaderboardHistoryResult
from ..models.cutenessLeaderboardResult import CutenessLeaderboardResult
from ..models.cutenessResult import CutenessResult
from ..models.incrementedCutenessResult import IncrementedCutenessResult
from ..settings.cutenessSettingsInterface import CutenessSettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class CutenessRepository(CutenessRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        cutenessMapper: CutenessMapperInterface,
        cutenessSettings: CutenessSettingsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        historyLeaderboardSize: int = 5,
        leaderboardSize: int = 10,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(cutenessMapper, CutenessMapperInterface):
            raise TypeError(f'cutenessMapper argument is malformed: \"{cutenessMapper}\"')
        elif not isinstance(cutenessSettings, CutenessSettingsInterface):
            raise TypeError(f'cutenessSettings argument is malformed: \"{cutenessSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(historyLeaderboardSize):
            raise TypeError(f'historyLeaderboardSize argument is malformed: \"{historyLeaderboardSize}\"')
        elif historyLeaderboardSize < 2 or historyLeaderboardSize > 6:
            raise ValueError(f'historyLeaderboardSize argument is out of bounds: {historyLeaderboardSize}')
        elif not utils.isValidInt(leaderboardSize):
            raise TypeError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 3 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: {leaderboardSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__cutenessMapper: Final[CutenessMapperInterface] = cutenessMapper
        self.__cutenessSettings: Final[CutenessSettingsInterface] = cutenessSettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__historyLeaderboardSize: Final[int] = historyLeaderboardSize
        self.__leaderboardSize: Final[int] = leaderboardSize

        self.__isDatabaseReady: bool = False

    async def fetchCuteness(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> CutenessResult:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = await self.__getCurrentYearAndMonthDateTime()
        utcYearAndMonth = await self.__cutenessMapper.serializeToUtcYearAndMonth(now)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND utcyearandmonth = $3
                LIMIT 1
            ''',
            twitchChannelId, chatterUserId, utcYearAndMonth,
        )

        await connection.close()

        cuteness: int | None = None

        if record is not None and len(record) >= 1:
            cuteness = record[0]

        return CutenessResult(
            cutenessDate = now,
            cuteness = cuteness,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessChampions(
        self,
        twitchChannelId: str,
    ) -> CutenessChampionsResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        leaderboardSize = await self.__cutenessSettings.getLeaderboardSize()

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT userid, SUM(cuteness) AS totalcuteness FROM cuteness
                WHERE twitchchannelid = $1 AND userid != $2
                GROUP BY userid
                ORDER BY totalcuteness DESC
                LIMIT $3
            ''',
            twitchChannelId, twitchChannelId, leaderboardSize,
        )

        await connection.close()

        champions: FrozenList[CutenessLeaderboardEntry] = FrozenList()

        if records is None or len(records) == 0:
            champions.freeze()

            return CutenessChampionsResult(
                champions = champions,
                twitchChannelId = twitchChannelId,
            )

        for index, record in enumerate(records):
            # Cuteness can potentially arrive from the database as a decimal.Decimal type,
            # so let's make sure to convert that value into an int.
            cuteness = int(round(record[1]))

            champions.append(CutenessLeaderboardEntry(
                cuteness = cuteness,
                rank = index + 1,
                chatterUserId = record[0],
                twitchChannelId = twitchChannelId,
            ))

        champions.freeze()

        return CutenessChampionsResult(
            champions = champions,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessHistory(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> CutenessHistoryResult:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        historySize = await self.__cutenessSettings.getHistorySize()

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cuteness, utcyearandmonth FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND cuteness IS NOT NULL AND cuteness >= 1
                ORDER BY utcyearandmonth DESC
                LIMIT $3
            ''',
            twitchChannelId, chatterUserId, historySize,
        )

        historyEntries: FrozenList[CutenessHistoryEntry] = FrozenList()

        if records is None or len(records) == 0:
            await connection.close()
            historyEntries.freeze()

            return CutenessHistoryResult(
                bestCuteness = None,
                historyEntries = historyEntries,
                totalCuteness = None,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        for record in records:
            cutenessDate = await self.__cutenessMapper.requireUtcYearAndMonthString(
                utcYearAndMonthString = record[1],
            )

            cuteness = int(round(record[0]))

            historyEntries.append(CutenessHistoryEntry(
                cutenessDate = cutenessDate,
                cuteness = cuteness,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            ))

        historyEntries.freeze()

        record = await connection.fetchRow(
            '''
                SELECT SUM(cuteness) FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND cuteness IS NOT NULL AND cuteness >= 1
                LIMIT 1
            ''',
            twitchChannelId, chatterUserId,
        )

        totalCuteness = 0

        if record is not None and len(record) >= 1:
            totalCuteness = int(round(record[0]))

        record = await connection.fetchRow(
            '''
                SELECT cuteness, utcyearandmonth FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND cuteness IS NOT NULL AND cuteness >= 1
                ORDER BY cuteness DESC
                LIMIT 1
            ''',
            twitchChannelId, chatterUserId,
        )

        bestCuteness: CutenessHistoryEntry | None = None

        if record is not None and len(record) >= 1:
            bestCutenessDate = await self.__cutenessMapper.requireUtcYearAndMonthString(
                utcYearAndMonthString = record[1],
            )

            # again, this should be impossible here, but let's just be safe
            bestCutenessAmount = int(round(record[0]))

            bestCuteness = CutenessHistoryEntry(
                cutenessDate = bestCutenessDate,
                cuteness = bestCutenessAmount,
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        await connection.close()

        return CutenessHistoryResult(
            bestCuteness = bestCuteness,
            historyEntries = historyEntries,
            totalCuteness = totalCuteness,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> IncrementedCutenessResult:
        if not utils.isValidInt(incrementAmount):
            raise TypeError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount < utils.getShortMinSafeSize() or incrementAmount > utils.getShortMaxSafeSize():
            raise ValueError(f'incrementAmount argument is out of bounds: {incrementAmount}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = await self.__getCurrentYearAndMonthDateTime()
        utcYearAndMonth = await self.__cutenessMapper.serializeToUtcYearAndMonth(now)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchchannelid = $1 AND userid = $2 AND utcyearandmonth = $3
                LIMIT 1
            ''',
            twitchChannelId, chatterUserId, utcYearAndMonth,
        )

        previousCuteness = 0

        if record is not None and len(record) >= 1:
            previousCuteness = record[0]

        newCuteness = int(max(previousCuteness + incrementAmount, 0))

        if newCuteness > utils.getLongMaxSafeSize():
            await connection.close()
            raise OverflowError(f'New cuteness would be too large ({newCuteness=}) ({previousCuteness=}) ({incrementAmount=})')

        await connection.execute(
            '''
                INSERT INTO cuteness (cuteness, twitchchannelid, userid, utcyearandmonth)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (twitchchannelid, userid, utcyearandmonth) DO UPDATE SET cuteness = EXCLUDED.cuteness
            ''',
            newCuteness, twitchChannelId, chatterUserId, utcYearAndMonth,
        )

        await connection.close()

        return IncrementedCutenessResult(
            cutenessDate = now,
            newCuteness = newCuteness,
            previousCuteness = previousCuteness,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessLeaderboard(
        self,
        twitchChannelId: str,
        specificLookupUserId: str | None = None,
    ) -> CutenessLeaderboardResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif specificLookupUserId is not None and not isinstance(specificLookupUserId, str):
            raise TypeError(f'specificLookupUserId argument is malformed: \"{specificLookupUserId}\"')

        now = await self.__getCurrentYearAndMonthDateTime()
        utcYearAndMonth = await self.__cutenessMapper.serializeToUtcYearAndMonth(now)
        leaderboardSize = await self.__cutenessSettings.getLeaderboardSize()

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cuteness, userid FROM cuteness
                WHERE twitchchannelid = $1 AND utcyearandmonth = $2 AND cuteness IS NOT NULL AND cuteness >= 1 AND userid != $3
                ORDER BY cuteness DESC
                LIMIT $4
            ''',
            twitchChannelId, utcYearAndMonth, twitchChannelId, leaderboardSize,
        )

        await connection.close()
        entries: FrozenList[CutenessLeaderboardEntry] = FrozenList()

        if records is None or len(records) == 0:
            entries.freeze()

            return CutenessLeaderboardResult(
                specificLookupCutenessResult = None,
                cutenessDate = now,
                entries = entries,
                twitchChannelId = twitchChannelId,
            )

        for index, record in enumerate(records):
            entries.append(CutenessLeaderboardEntry(
                cuteness = record[0],
                rank = index + 1,
                chatterUserId = record[1],
                twitchChannelId = twitchChannelId,
            ))

        entries.freeze()

        specificLookupAlreadyInResults = False
        if utils.isValidStr(specificLookupUserId):
            for entry in entries:
                if entry.chatterUserId == specificLookupUserId:
                    specificLookupAlreadyInResults = True
                    break

        specificLookupCutenessResult: CutenessResult | None = None
        if not specificLookupAlreadyInResults and utils.isValidStr(specificLookupUserId):
            specificLookupCutenessResult = await self.fetchCuteness(
                chatterUserId = specificLookupUserId,
                twitchChannelId = twitchChannelId,
            )

        return CutenessLeaderboardResult(
            specificLookupCutenessResult = specificLookupCutenessResult,
            cutenessDate = now,
            entries = entries,
            twitchChannelId = twitchChannelId,
        )

    async def fetchCutenessLeaderboardHistory(
        self,
        twitchChannelId: str,
    ) -> CutenessLeaderboardHistoryResult:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = await self.__getCurrentYearAndMonthDateTime()
        utcYearAndMonth = await self.__cutenessMapper.serializeToUtcYearAndMonth(now)
        historyLeaderboardSize = await self.__cutenessSettings.getHistoryLeaderboardSize()

        connection = await self.__getDatabaseConnection()
        historyRecords = await connection.fetchRows(
            '''
                SELECT DISTINCT utcyearandmonth FROM cuteness
                WHERE twitchchannelid = $1 AND utcyearandmonth != $2
                ORDER BY utcyearandmonth DESC
                LIMIT $3
            ''',
            twitchChannelId, utcYearAndMonth, historyLeaderboardSize,
        )

        history: FrozenList[CutenessLeaderboardResult] = FrozenList()

        if historyRecords is None or len(historyRecords) == 0:
            await connection.close()
            history.freeze()

            return CutenessLeaderboardHistoryResult(
                history = history,
                twitchChannelId = twitchChannelId,
            )

        for historyRecord in historyRecords:
            monthDateTime = await self.__cutenessMapper.requireUtcYearAndMonthString(historyRecord[0])
            monthDateTimeString = await self.__cutenessMapper.serializeToUtcYearAndMonth(monthDateTime)

            monthRecords = await connection.fetchRows(
                '''
                    SELECT cuteness, userid FROM cuteness
                    WHERE cuteness IS NOT NULL AND cuteness >= 1 AND twitchchannelid = $1 AND userid != $2 AND utcyearandmonth = $3
                    ORDER BY cuteness DESC
                    LIMIT $4
                ''',
                twitchChannelId, twitchChannelId, monthDateTimeString, historyLeaderboardSize,
            )

            if monthRecords is None or len(monthRecords) == 0:
                continue

            entries: FrozenList[CutenessLeaderboardEntry] = FrozenList()
            rank = 1

            for monthRecord in monthRecords:
                entries.append(CutenessLeaderboardEntry(
                    cuteness = monthRecord[0],
                    rank = rank,
                    chatterUserId = monthRecord[1],
                    twitchChannelId = twitchChannelId,
                ))
                rank += 1

            entries.freeze()

            history.append(CutenessLeaderboardResult(
                specificLookupCutenessResult = None,
                cutenessDate = monthDateTime,
                entries = entries,
                twitchChannelId = twitchChannelId,
            ))

        await connection.close()
        history.freeze()

        return CutenessLeaderboardHistoryResult(
            history = history,
            twitchChannelId = twitchChannelId,
        )

    async def __getCurrentYearAndMonthDateTime(self) -> datetime:
        now = self.__timeZoneRepository.getNow()

        return now.replace(
            day = 1,
            hour = 0,
            minute = 0,
            second = 0,
            microsecond = 0,
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
