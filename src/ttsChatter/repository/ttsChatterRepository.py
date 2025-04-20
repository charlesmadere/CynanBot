from typing import Final

from lru import LRU

from .ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ...misc import utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TtsChatterRepository(TtsChatterRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        cacheSize: int = 64
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > 256:
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, bool]] = LRU(cacheSize)

    async def add(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO ttschatter (chatteruserid, twitchchannelid)
                VALUES ($1, $2)
                ON CONFLICT (chatteruserid, twitchchannelid) DO NOTHING
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = True
        self.__timber.log('TtsChatterRepository', f'Added TTS Chatter ({chatterUserId=}) ({twitchChannelId=})')

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TtsChatterRepository', 'Caches cleared')

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
                        CREATE TABLE IF NOT EXISTS ttschatter (
                            chatteruserid text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS ttschatter (
                            chatteruserid TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def isTtsChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> bool:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if f'{twitchChannelId}:{chatterUserId}' in self.__cache:
            return self.__cache.get(f'{twitchChannelId}:{chatterUserId}', False)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT COUNT(1) FROM ttschatter
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        count: int | None = None
        if record is not None and len(record) >= 1:
            count = record[0]

        isTtsChatter = False
        if utils.isValidInt(count) and count >= 1:
            isTtsChatter = True

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = isTtsChatter
        return isTtsChatter

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> bool:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        isTtsChatter = await self.isTtsChatter(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        if not isTtsChatter:
            return False

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM ttschatter
                WHERE chatteruserid = $1 AND twitchchannelid = $2
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = False
        self.__timber.log('TtsChatterRepository', f'Removed TTS Chatter ({chatterUserId=}) ({twitchChannelId=})')

        return True
