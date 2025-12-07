from typing import Final

from lru import LRU

from .nickNameRepositoryInterface import NickNameRepositoryInterface
from ..models.nickNameData import NickNameData
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class NickNameRepository(NickNameRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        cacheSize: int = 32,
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
        self.__cache: LRU[str, NickNameData | None] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('NickNameRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> NickNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if f'{twitchChannelId}:{chatterUserId}' in self.__cache:
            return self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT nickname FROM nicknames
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        nickName: str | None = None

        if record is not None and len(record) >= 1:
            nickName = record[0]

        if not utils.isValidStr(nickName):
            self.__cache[f'{twitchChannelId}:{chatterUserId}'] = None
            return None

        nickNameData = NickNameData(
            chatterUserId = chatterUserId,
            nickName = nickName,
            twitchChannelId = twitchChannelId
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = nickNameData
        return nickNameData

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
                        CREATE TABLE IF NOT EXISTS nicknames (
                            chatteruserid text NOT NULL,
                            nickname text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS nicknames (
                            chatteruserid TEXT NOT NULL,
                            nickname TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> NickNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        nickNameData = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        if nickNameData is None:
            return None

        self.__cache.pop(f'{twitchChannelId}:{chatterUserId}')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM nicknames
                WHERE chatteruserid = $1 AND twitchchannelid = $2
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('NickNameRepository', f'Removed nickname ({nickNameData=})')

        return nickNameData

    async def set(
        self,
        chatterUserId: str,
        nickName: str | None,
        twitchChannelId: str,
    ) -> NickNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif nickName is not None and not isinstance(nickName, str):
            raise TypeError(f'nickName argument is malformed: \"{nickName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(nickName):
            return await self.remove(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO nicknames (chatteruserid, nickname, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET nickname = EXCLUDED.nickname
            ''',
            chatterUserId, nickName, twitchChannelId,
        )

        await connection.close()

        nickNameData = NickNameData(
            chatterUserId = chatterUserId,
            nickName = nickName,
            twitchChannelId = twitchChannelId,
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = nickNameData
        self.__timber.log('NickNameRepository', f'Set nickname ({nickNameData=})')

        return nickNameData
