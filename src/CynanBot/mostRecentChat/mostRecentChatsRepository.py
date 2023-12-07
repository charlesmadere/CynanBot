from collections import defaultdict
from typing import Dict, Optional

from lru import LRU

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
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
        cacheSize: int = 100
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(cacheSize):
            raise ValueError(f'cacheSize argument is malformed: \"{cacheSize}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__caches: Dict[str, LRU] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('MostRecentChatsRepository', 'Caches cleared')

    async def get(self, chatterUserId: str, twitchChannelId: str) -> Optional[MostRecentChat]:
        if not utils.isValidStr(chatterUserId):
            raise ValueError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise ValueError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cache = self.__caches[twitchChannelId]

        if chatterUserId in cache:
            return cache[chatterUserId]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime, twitchchannelid, userid FROM mostrecentchats
                WHERE twitchchannelid = $1 AND userid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        mostRecentChat: Optional[MostRecentChat] = None

        if utils.hasItems(record):
            simpleDateTime = SimpleDateTime(utils.getDateTimeFromStr(record[0]))

            mostRecentChat = MostRecentChat(
                mostRecentChat = simpleDateTime,
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
                        chatteruserid public.citext NOT NULL,
                        datetime text NOT NULL,
                        twitchchannelid public.citext NOT NULL,
                        PRIMARY KEY (chatteruserid, twitchchannelid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS mostrecentchats (
                        chatteruserid TEXT NOT NULL COLLATE NOCASE,
                        datetime TEXT NOT NULL,
                        twitchchannelid TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (chatteruserid, twitchchannelid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def set(self, chatterUserId: str, twitchChannelId: str):
        if not utils.isValidStr(chatterUserId):
            raise ValueError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise ValueError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        simpleDateTime = SimpleDateTime()

        self.__caches[twitchChannelId][chatterUserId] = MostRecentChat(
            mostRecentChat = simpleDateTime,
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
            chatterUserId, simpleDateTime.getDateTime().isoformat(), twitchChannelId
        )

        await connection.close()
