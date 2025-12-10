from __future__ import annotations

from typing import Final

from lru import LRU

from .chatterPreferredNameRepositoryInterface import ChatterPreferredNameRepositoryInterface
from ..models.chatterPreferredNameData import ChatterPreferredNameData
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class ChatterPreferredNameRepository(ChatterPreferredNameRepositoryInterface):

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
        self.__cache: LRU[str, ChatterPreferredNameData | None] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('ChatterPreferredNameRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if f'{twitchChannelId}:{chatterUserId}' in self.__cache:
            return self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT preferredname FROM chatterpreferrednames
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        preferredName: str | None = None

        if record is not None and len(record) >= 1:
            preferredName = utils.cleanStr(record[0])

        if not utils.isValidStr(preferredName):
            self.__cache[f'{twitchChannelId}:{chatterUserId}'] = None
            return None

        preferredNameData = ChatterPreferredNameData(
            chatterUserId = chatterUserId,
            preferredName = preferredName,
            twitchChannelId = twitchChannelId,
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = preferredNameData
        return preferredNameData

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
                        CREATE TABLE IF NOT EXISTS chatterpreferrednames (
                            chatteruserid text NOT NULL,
                            preferredname text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS chatterpreferrednames (
                            chatteruserid TEXT NOT NULL,
                            preferredname TEXT NOT NULL,
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
    ) -> ChatterPreferredNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        preferredNameData = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        if preferredNameData is None:
            return None

        self.__cache.pop(f'{twitchChannelId}:{chatterUserId}')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM chatterpreferrednames
                WHERE chatteruserid = $1 AND twitchchannelid = $2
            ''',
            chatterUserId, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('ChatterPreferredNameRepository', f'Removed preferred name ({preferredNameData=})')

        return preferredNameData

    async def set(
        self,
        chatterUserId: str,
        preferredName: str | None,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif preferredName is not None and not isinstance(preferredName, str):
            raise TypeError(f'preferredName argument is malformed: \"{preferredName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        preferredName = utils.cleanStr(preferredName)

        if not utils.isValidStr(preferredName):
            return await self.remove(
                chatterUserId = chatterUserId,
                twitchChannelId = twitchChannelId,
            )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO chatterpreferrednames (chatteruserid, preferredname, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET preferredname = EXCLUDED.preferredname
            ''',
            chatterUserId, preferredName, twitchChannelId,
        )

        await connection.close()

        preferredNameData = ChatterPreferredNameData(
            chatterUserId = chatterUserId,
            preferredName = preferredName,
            twitchChannelId = twitchChannelId,
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = preferredNameData
        self.__timber.log('ChatterPreferredNameRepository', f'Set preferred name ({preferredNameData=})')

        return preferredNameData
