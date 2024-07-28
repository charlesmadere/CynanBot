from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from lru import LRU

from .timeoutCheerActionEntry import \
    TimeoutCheerActionEntry
from .timeoutCheerActionHistory import \
    TimeoutCheerActionHistory
from .timeoutCheerActionHistoryRepositoryInterface import \
    TimeoutCheerActionHistoryRepositoryInterface
from .timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutCheerActionHistoryRepository(TimeoutCheerActionHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeoutCheerActionJsonMapper: TimeoutCheerActionJsonMapperInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheSize: int = 32,
        maximumHistoryEntriesSize: int = 5
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutCheerActionJsonMapper, TimeoutCheerActionJsonMapperInterface):
            raise TypeError(f'timeoutCheerActionJsonMapper argument is malformed: \"{timeoutCheerActionJsonMapper}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')
        elif not utils.isValidInt(maximumHistoryEntriesSize):
            raise TypeError(f'maximumHistoryEntriesSize argument is malformed: \"{maximumHistoryEntriesSize}\"')
        elif maximumHistoryEntriesSize < 3 or maximumHistoryEntriesSize > 8:
            raise ValueError(f'maximumHistoryEntriesSize argument is out of bounds: {maximumHistoryEntriesSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeoutCheerActionJsonMapper: TimeoutCheerActionJsonMapperInterface = timeoutCheerActionJsonMapper
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__maximumHistoryEntriesSize: int = maximumHistoryEntriesSize

        self.__isDatabaseReady: bool = False
        self.__caches: dict[str, LRU[str, TimeoutCheerActionHistory | None]] = defaultdict(lambda: LRU(cacheSize))

    async def add(
        self,
        bitAmount: int,
        durationSeconds: int,
        chatterUserId: str,
        timedOutByUserId: str,
        twitchAccessToken: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not utils.isValidInt(bitAmount):
            raise TypeError(f'bitAmount argument is malformed: \"{bitAmount}\"')
        elif bitAmount < 1 or bitAmount > utils.getIntMaxSafeSize():
            raise TypeError(f'bitAmount argument is out of bounds: {bitAmount}')
        elif not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds < 1 or durationSeconds > utils.getIntMaxSafeSize():
            raise TypeError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(timedOutByUserId):
            raise TypeError(f'timedOutByUserId argument is malformed: \"{timedOutByUserId}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        history = await self.get(
            chatterUserId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        totalTimeouts: int
        if history is None:
            totalTimeouts = 1
        else:
            totalTimeouts = history.totalTimeouts + 1

        historyEntries: list[TimeoutCheerActionEntry] = list()
        if history is not None and history.entries is not None and len(historyEntries) >= 1:
            for entry in history.entries:
                historyEntries.append(entry)

        historyEntries.append(TimeoutCheerActionEntry(
            timedOutAtDateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            bitAmount = bitAmount,
            durationSeconds = durationSeconds,
            timedOutByUserId = timedOutByUserId
        ))

        historyEntries.sort(key = lambda entry: entry.timedOutAtDateTime, reverse = True)

        while len(historyEntries) > self.__maximumHistoryEntriesSize:
            del historyEntries[len(historyEntries) - 1]

        self.__caches[twitchChannelId][chatterUserId] = TimeoutCheerActionHistory(
            totalTimeouts = totalTimeouts,
            entries = historyEntries,
            chatterUserId = history.chatterUserId,
            chatterUserName = history.chatterUserName,
            twitchChannel = history.twitchChannel,
            twitchChannelId = twitchChannelId
        )

        historyEntriesString = await self.__timeoutCheerActionJsonMapper.serializeTimeoutCheerActionEntriesToJsonString(
            entries = historyEntries
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO timeoutcheeractionhistory (totaltimeouts, chatteruserid, entries, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET totaltimeouts = EXCLUDED.totaltimeouts, entries = EXCLUDED.entries
            ''',
            totalTimeouts, chatterUserId, historyEntriesString, twitchChannelId
        )

        await connection.close()

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('TimeoutCheerActionHistoryRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchAccessToken: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TimeoutCheerActionHistory:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
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
                SELECT totaltimeouts, chatteruserid, entries FROM timeoutcheeractionhistory
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        chatterUserName = await self.__userIdsRepository.requireUserName(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken
        )

        timeoutCheerActionHistory: TimeoutCheerActionHistory

        if record is None or len(record) == 0:
            timeoutCheerActionHistory = TimeoutCheerActionHistory(
                totalTimeouts = 0,
                entries = None,
                chatterUserId = chatterUserId,
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        else:
            entries = await self.__timeoutCheerActionJsonMapper.parseTimeoutCheerActionEntriesString(
                jsonString = record[2]
            )

            timeoutCheerActionHistory = TimeoutCheerActionHistory(
                totalTimeouts = record[0],
                entries = entries,
                chatterUserId = record[1],
                chatterUserName = chatterUserName,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

        cache[chatterUserId] = timeoutCheerActionHistory
        return timeoutCheerActionHistory

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
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS timeoutcheeractionhistory (
                            totaltimeouts int DEFAULT 0 NOT NULL,
                            chatteruserid text NOT NULL,
                            entries text DEFAULT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS timeoutcheeractionhistory (
                            totaltimeouts INTEGER NOT NULL DEFAULT 0,
                            chatteruserid TEXT NOT NULL,
                            entries TEXT DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
