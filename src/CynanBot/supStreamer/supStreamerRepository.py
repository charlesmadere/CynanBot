from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from lru import LRU

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.supStreamer.supStreamerChatter import SupStreamerChatter
from CynanBot.supStreamer.supStreamerRepositoryInterface import \
    SupStreamerRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface


class SupStreamerRepository(SupStreamerRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 100
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 8 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__caches: dict[str, LRU[str, SupStreamerChatter | None]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('SupStreamerRepository', 'Caches cleared')

    async def getChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> SupStreamerChatter:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        chatter = self.__caches[twitchChannelId].get(chatterUserId, None)

        if chatter is not None:
            return chatter

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT mostrecentsup FROM supstreamerchatters
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        if record is None or len(record) == 0:
            chatter = SupStreamerChatter(
                mostRecentSup = None,
                twitchChannelId = twitchChannelId,
                userId = chatterUserId
            )
        else:
            chatter = SupStreamerChatter(
                mostRecentSup = datetime.fromisoformat(record[0]),
                twitchChannelId = twitchChannelId,
                userId = chatterUserId
            )

        self.__caches[twitchChannelId][chatterUserId] = chatter
        return chatter

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS supstreamerchatters (
                        mostrecentsup text NOT NULL,
                        chatteruserid text NOT NULL,
                        twitchchannelid text NOT NULL
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS supstreamerchatters (
                        mostrecentsup TEXT NOT NULL,
                        chatteruserid TEXT NOT NULL,
                        twitchchannelid TEXT NOT NULL
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def updateChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        now = datetime.now(self.__timeZoneRepository.getDefault())

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO supstreamerchatters (mostrecentsup, chatteruserid, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (mostrecentsup, chatteruserid, twitchchannelid) DO UPDATE SET mostrecentsup = EXCLUDED.mostrecentsup
            ''',
            now.isoformat(), chatterUserId, twitchChannelId
        )

        await connection.close()

        self.__caches[twitchChannelId][chatterUserId] = SupStreamerChatter(
            mostRecentSup = now,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId
        )
