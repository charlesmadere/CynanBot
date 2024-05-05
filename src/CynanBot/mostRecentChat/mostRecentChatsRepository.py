from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone, tzinfo

from lru import LRU

import CynanBot.misc.utils as utils
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface


class MostRecentChatsRepository(MostRecentChatsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        cacheSize: int = 100,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZone: tzinfo = timeZone

        self.__isDatabaseReady: bool = False
        self.__caches: dict[str, LRU[str, MostRecentChat | None]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('MostRecentChatsRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> MostRecentChat | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cache = self.__caches[twitchChannelId]

        if chatterUserId in cache:
            return cache[chatterUserId]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime, twitchchannelid, chatteruserid FROM mostrecentchats
                WHERE twitchchannelid = $1 AND chatteruserid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        mostRecentChat: MostRecentChat | None = None

        if record is not None and len(record) >= 1:
            mostRecentChat = MostRecentChat(
                mostRecentChat = datetime.fromisoformat(record[0]),
                twitchChannelId = record[1],
                userId = record[2]
            )

        cache[chatterUserId] = mostRecentChat
        return mostRecentChat

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
                    CREATE TABLE IF NOT EXISTS mostrecentchats (
                        chatteruserid text NOT NULL,
                        datetime text NOT NULL,
                        twitchchannelid text NOT NULL,
                        PRIMARY KEY (chatteruserid, twitchchannelid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS mostrecentchats (
                        chatteruserid TEXT NOT NULL,
                        datetime TEXT NOT NULL,
                        twitchchannelid TEXT NOT NULL,
                        PRIMARY KEY (chatteruserid, twitchchannelid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        mostRecentChat = datetime.now(self.__timeZone)

        self.__caches[twitchChannelId][chatterUserId] = MostRecentChat(
            mostRecentChat = mostRecentChat,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO mostrecentchats (chatteruserid, datetime, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET datetime = EXCLUDED.datetime
            ''',
            chatterUserId, mostRecentChat.isoformat(), twitchChannelId
        )

        await connection.close()
