from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from frozenlist import FrozenList
from lru import LRU

from .timeoutActionHistory import TimeoutActionHistory
from .timeoutActionHistoryEntry import TimeoutActionHistoryEntry
from .timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from .timeoutActionJsonMapperInterface import TimeoutActionJsonMapperInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface


class TimeoutActionHistoryRepository(TimeoutActionHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeoutActionJsonMapper: TimeoutActionJsonMapperInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 32,
        maximumHistoryEntriesSize: int = 16
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionJsonMapper, TimeoutActionJsonMapperInterface):
            raise TypeError(f'timeoutActionJsonMapper argument is malformed: \"{timeoutActionJsonMapper}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')
        elif not utils.isValidInt(maximumHistoryEntriesSize):
            raise TypeError(f'maximumHistoryEntriesSize argument is malformed: \"{maximumHistoryEntriesSize}\"')
        elif maximumHistoryEntriesSize < 1 or maximumHistoryEntriesSize > 32:
            raise ValueError(f'maximumHistoryEntriesSize argument is out of bounds: {maximumHistoryEntriesSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeoutActionJsonMapper: TimeoutActionJsonMapperInterface = timeoutActionJsonMapper
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__maximumHistoryEntriesSize: int = maximumHistoryEntriesSize

        self.__isDatabaseReady: bool = False
        self.__caches: dict[str, LRU[str, TimeoutActionHistory | None]] = defaultdict(lambda: LRU(cacheSize))

    async def add(
        self,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise TypeError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(timedOutByUserId):
            raise TypeError(f'timedOutByUserId argument is malformed: \"{timedOutByUserId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        history = await self.get(
            chatterUserId = chatterUserId,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        totalTimeouts: int
        if history is None:
            totalTimeouts = 1
        else:
            totalTimeouts = history.totalTimeouts + 1

        newHistoryEntries: list[TimeoutActionHistoryEntry] = list()
        if history is not None and history.entries is not None and len(history.entries) >= 1:
            for entry in history.entries:
                newHistoryEntries.append(entry)

        newHistoryEntries.append(TimeoutActionHistoryEntry(
            timedOutAtDateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            durationSeconds = durationSeconds,
            timedOutByUserId = timedOutByUserId
        ))

        newHistoryEntries.sort(key = lambda entry: entry.timedOutAtDateTime, reverse = True)

        while len(newHistoryEntries) > self.__maximumHistoryEntriesSize:
            del newHistoryEntries[len(newHistoryEntries) - 1]

        frozenHistoryEntries: FrozenList[TimeoutActionHistoryEntry] = FrozenList(newHistoryEntries)
        frozenHistoryEntries.freeze()

        self.__caches[twitchChannelId][chatterUserId] = TimeoutActionHistory(
            entries = frozenHistoryEntries,
            totalTimeouts = totalTimeouts,
            chatterUserId = chatterUserId,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        historyEntriesString = await self.__timeoutActionJsonMapper.serializeTimeoutActionEntriesToJsonString(
            entries = newHistoryEntries
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO timeoutactionhistory (totaltimeouts, chatteruserid, entries, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET totaltimeouts = EXCLUDED.totaltimeouts, entries = EXCLUDED.entries
            ''',
            totalTimeouts, chatterUserId, historyEntriesString, twitchChannelId
        )

        await connection.close()

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('TimeoutActionHistoryRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> TimeoutActionHistory | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cache = self.__caches[twitchChannelId]

        if chatterUserId in cache:
            return cache[chatterUserId]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT totaltimeouts, chatteruserid, entries FROM timeoutactionhistory
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        timeoutActionHistory: TimeoutActionHistory

        if record is None or len(record) == 0:
            timeoutActionHistory = TimeoutActionHistory(
                entries = None,
                totalTimeouts = 0,
                chatterUserId = chatterUserId,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        else:
            entries = await self.__timeoutActionJsonMapper.parseTimeoutActionEntriesString(
                jsonString = record[2]
            )

            timeoutActionHistory = TimeoutActionHistory(
                entries = entries,
                totalTimeouts = record[0],
                chatterUserId = record[1],
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

        cache[chatterUserId] = timeoutActionHistory
        return timeoutActionHistory

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
                        CREATE TABLE IF NOT EXISTS timeoutactionhistory (
                            totaltimeouts int DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            entries jsonb DEFAULT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS timeoutactionhistory (
                            totaltimeouts INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            entries TEXT DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
