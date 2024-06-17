from __future__ import annotations

from collections import defaultdict

from lru import LRU

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.timeout.timeoutCheerActionHistory import \
    TimeoutCheerActionHistory
from CynanBot.cheerActions.timeout.timeoutCheerActionHistoryRepositoryInterface import \
    TimeoutCheerActionHistoryRepositoryInterface
from CynanBot.cheerActions.timeout.timeoutCheerActionJsonMapperInterface import \
    TimeoutCheerActionJsonMapperInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TimeoutCheerActionHistoryRepository(TimeoutCheerActionHistoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeoutCheerActionJsonMapper: TimeoutCheerActionJsonMapperInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheSize: int = 32
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutCheerActionJsonMapper, TimeoutCheerActionJsonMapperInterface):
            raise TypeError(f'timeoutCheerActionJsonMapper argument is malformed: \"{timeoutCheerActionJsonMapper}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeoutCheerActionJsonMapper: TimeoutCheerActionJsonMapperInterface = timeoutCheerActionJsonMapper
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False
        self.__caches: dict[str, LRU[str, TimeoutCheerActionHistory | None]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('TimeoutCheerActionHistoryRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchAccessToken: str | None,
        twitchChannelId: str
    ) -> TimeoutCheerActionHistory | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cache = self.__caches[twitchChannelId]

        if chatterUserId in cache:
            return cache[chatterUserId]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT timeoutcheeractionhistory.totaltimeouts, timeoutcheeractionhistory.entries, userids.username FROM timeoutcheeractionhistory
                INNER JOIN userids ON timeoutcheeractionhistory.userid = userids.userid
                WHERE timeoutcheeractionhistory.chatteruserid = $1 AND timeoutcheeractionhistory.twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        timeoutCheerActionHistory: TimeoutCheerActionHistory | None = None

        chatterUserName = await self.__userIdsRepository.fetchUserName(
            userId = chatterUserId,
            twitchAccessToken = twitchAccessToken
        )

        if utils.isValidStr(chatterUserName) and record is not None and len(record) >= 1:
            entries = await self.__timeoutCheerActionJsonMapper.parseTimeoutCheerActionEntriesString(
                string = record[1]
            )

            timeoutCheerActionHistory = TimeoutCheerActionHistory(
                totalTimeouts = record[0],
                entries = entries,
                chatterUserId = record[2],
                chatterUserName = chatterUserName,
                twitchChannel = record[3],
                twitchChannelId = record[4]
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

        match connection.getDatabaseType():
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
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
