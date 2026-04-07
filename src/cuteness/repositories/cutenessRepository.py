from dataclasses import dataclass
from datetime import datetime
from typing import Final

from frozenlist import FrozenList

from .cutenessRepositoryInterface import CutenessRepositoryInterface
from ..mappers.cutenessMapperInterface import CutenessMapperInterface
from ..models.cutenessChampionsResult import CutenessChampionsResult
from ..models.cutenessHistoryEntry import CutenessHistoryEntry
from ..models.cutenessHistoryResult import CutenessHistoryResult
from ..models.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from ..models.cutenessResult import CutenessResult
from ..settings.cutenessSettingsInterface import CutenessSettingsInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class CutenessRepository(CutenessRepositoryInterface):

    @dataclass(frozen = True, slots = True)
    class CutenessDate:
        dateTime: datetime

        @property
        def databaseString(self) -> str:
            return self.dateTime.strftime('%Y-%m')

        @property
        def humanString(self) -> str:
            return self.dateTime.strftime('%b %Y')

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        cutenessMapper: CutenessMapperInterface,
        cutenessSettings: CutenessSettingsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
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

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__cutenessMapper: Final[CutenessMapperInterface] = cutenessMapper
        self.__cutenessSettings: Final[CutenessSettingsInterface] = cutenessSettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

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

        now = self.__timeZoneRepository.getNow()
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
