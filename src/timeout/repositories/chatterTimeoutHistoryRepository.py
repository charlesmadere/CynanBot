from datetime import datetime, timedelta
from typing import Final

from frozenlist import FrozenList
from lru import LRU

from .chatterTimeoutHistoryRepositoryInterface import ChatterTimeoutHistoryRepositoryInterface
from ..mappers.chatterTimeoutHistoryMapperInterface import ChatterTimeoutHistoryMapperInterface
from ..models.chatterTimeoutHistory import ChatterTimeoutHistory
from ..models.chatterTimeoutHistoryEntry import ChatterTimeoutHistoryEntry
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class ChatterTimeoutHistoryRepository(ChatterTimeoutHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        chatterTimeoutHistoryMapper: ChatterTimeoutHistoryMapperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 64,
        historyEntriesMaxSize: int = 16,
        historyEntriesMaxAge: timedelta = timedelta(weeks = 2),
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(chatterTimeoutHistoryMapper, ChatterTimeoutHistoryMapperInterface):
            raise TypeError(f'chatterTimeoutHistoryMapper argument is malformed: \"{chatterTimeoutHistoryMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > 256:
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')
        elif not utils.isValidInt(historyEntriesMaxSize):
            raise TypeError(f'historyEntriesMaxSize argument is malformed: \"{historyEntriesMaxSize}\"')
        elif historyEntriesMaxSize < 1 or historyEntriesMaxSize > 32:
            raise ValueError(f'historyEntriesMaxSize argument is out of bounds: {historyEntriesMaxSize}')
        elif not isinstance(historyEntriesMaxAge, timedelta):
            raise TypeError(f'historyEntriesMaxAge argument is malformed: \"{historyEntriesMaxAge}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__chatterTimeoutHistoryMapper: Final[ChatterTimeoutHistoryMapperInterface] = chatterTimeoutHistoryMapper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__historyEntriesMaxSize: Final[int] = historyEntriesMaxSize
        self.__historyEntriesMaxAge: Final[timedelta] = historyEntriesMaxAge

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, ChatterTimeoutHistory | None]] = LRU(cacheSize)

    async def add(
        self,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchChannelId: str,
    ) -> ChatterTimeoutHistory:
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(timedOutByUserId):
            raise TypeError(f'timedOutByUserId argument is malformed: \"{timedOutByUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        previousTimeoutHistory = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        newHistoryEntries: FrozenList[ChatterTimeoutHistoryEntry] = FrozenList(previousTimeoutHistory.entries)
        newHistoryEntries.append(ChatterTimeoutHistoryEntry(
            dateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            durationSeconds = durationSeconds,
            timedOutByUserId = timedOutByUserId,
        ))
        newHistoryEntries.freeze()

        newTotalDurationSeconds = previousTimeoutHistory.totalDurationSeconds + durationSeconds

        cleanedHistoryEntries = await self.__cleanHistoryEntries(
            historyEntries = newHistoryEntries,
        )

        historyEntriesJson = await self.__chatterTimeoutHistoryMapper.serializeHistoryEntries(
            historyEntries = cleanedHistoryEntries,
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO chattertimeouthistory (totaldurationseconds, history, chatteruserid, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET totaldurationseconds = EXCLUDED.totaldurationseconds, history = EXCLUDED.history
            ''',
            newTotalDurationSeconds, historyEntriesJson, chatterUserId, twitchChannelId,
        )
        await connection.close()

        newTimeoutHistory = ChatterTimeoutHistory(
            entries = cleanedHistoryEntries,
            totalDurationSeconds = newTotalDurationSeconds,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = newTimeoutHistory
        return newTimeoutHistory

    async def __cleanHistoryEntries(
        self,
        historyEntries: FrozenList[ChatterTimeoutHistoryEntry] | None,
    ) -> FrozenList[ChatterTimeoutHistoryEntry]:
        cleanedHistoryEntries: FrozenList[ChatterTimeoutHistoryEntry] = FrozenList()

        if historyEntries is None:
            cleanedHistoryEntries.freeze()
            return cleanedHistoryEntries

        index = 0
        now = datetime.now(self.__timeZoneRepository.getDefault())

        while index < len(historyEntries) and len(cleanedHistoryEntries) < self.__historyEntriesMaxSize:
            historyEntry = historyEntries[index]

            if historyEntry.dateTime + self.__historyEntriesMaxAge >= now:
                cleanedHistoryEntries.append(historyEntry)

            index += 1

        cleanedHistoryEntries.freeze()
        return cleanedHistoryEntries

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('ChatterTimeoutHistoryRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterTimeoutHistory:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        history = self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)
        if history is not None:
            return history

        connection = await self.__getDatabaseConnection()
        row = await connection.fetchRow(
            '''
                SELECT totaldurationseconds, history FROM chattertimeouthistory
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        totalDurationSeconds: int = 0
        historyEntries: FrozenList[ChatterTimeoutHistoryEntry] | None = None

        if row is not None and len(row) >= 1:
            totalDurationSeconds = row[0]
            historyEntries = await self.__chatterTimeoutHistoryMapper.parseHistoryEntries(row[1])

        cleanedHistoryEntries = await self.__cleanHistoryEntries(
            historyEntries = historyEntries,
        )

        history = ChatterTimeoutHistory(
            entries = cleanedHistoryEntries,
            totalDurationSeconds = totalDurationSeconds,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = history
        return history

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTables()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTables(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS chattertimeouthistory (
                            totaldurationseconds bigint DEFAULT 0 NOT NULL,
                            history jsonb DEFAULT NULL,
                            chatteruserid text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS chattertimeouthistory (
                            totaldurationseconds INTEGER NOT NULL DEFAULT 0,
                            history text DEFAULT NULL,
                            chatteruserid TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
