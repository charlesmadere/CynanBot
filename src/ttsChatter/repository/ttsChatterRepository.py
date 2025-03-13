from lru import LRU

from .ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..models.ttsChatter import TtsChatter
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

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__cache: LRU[str, TtsChatter | None] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TtsChatterRepository', f'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> TtsChatter | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if f'{twitchChannelId}:{chatterUserId}' in self.__cache:
            return self.__cache[f'{twitchChannelId}:{chatterUserId}']

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT chatteruserid FROM ttschatter
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()

        ttsChatter = TtsChatter(chatterUserId, twitchChannelId)
        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = ttsChatter

        if record is not None:
            return ttsChatter
        else:
            self.__cache[f'{twitchChannelId}:{chatterUserId}'] = None
            return None

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
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> TtsChatter | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        ttsChatter = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        if ttsChatter is None:
            return None

        self.__cache.pop(f'{twitchChannelId}:{chatterUserId}')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM ttschatter
                WHERE chatteruserid = $1 AND twitchchannelid = $2
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        self.__timber.log('TtsChatterRepository', f'Removed TTS Chatter ({ttsChatter=})')

        return ttsChatter

    async def set(self, ttsChatter: TtsChatter):
        if not isinstance(ttsChatter, TtsChatter):
            raise TypeError(f'ttsChatter argument is malformed: \"{ttsChatter}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO ttschatter (chatteruserid, twitchchannelid)
                VALUES ($1, $2)
            ''',
            ttsChatter.chatterUserId, ttsChatter.twitchChannelId
        )

        await connection.close()
        self.__cache[f'{ttsChatter.twitchChannelId}:{ttsChatter.chatterUserId}'] = ttsChatter
        self.__timber.log('TtsChatterRepository', f'Set TTS Chatter Active ({ttsChatter=})')
