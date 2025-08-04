from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Final

from lru import LRU

from .supStreamerChatter import SupStreamerChatter
from .supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface


class SupStreamerRepository(SupStreamerRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 100,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__caches: Final[dict[str, LRU[str, SupStreamerChatter | None]]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('SupStreamerRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> SupStreamerChatter | None:
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
                SELECT mostrecentsup FROM supstreamerchatters
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        supStreamerChatter: SupStreamerChatter | None = None

        if record is not None and len(record) >= 1:
            supStreamerChatter = SupStreamerChatter(
                mostRecentSup = datetime.fromisoformat(record[0]),
                twitchChannelId = twitchChannelId,
                userId = chatterUserId
            )

        cache[chatterUserId] = supStreamerChatter
        return supStreamerChatter

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
                        CREATE TABLE IF NOT EXISTS supstreamerchatters (
                            chatteruserid text NOT NULL,
                            mostrecentsup text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS supstreamerchatters (
                            chatteruserid TEXT NOT NULL,
                            mostrecentsup TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        mostRecentSup = datetime.now(self.__timeZoneRepository.getDefault())

        self.__caches[twitchChannelId][chatterUserId] = SupStreamerChatter(
            mostRecentSup = mostRecentSup,
            twitchChannelId = twitchChannelId,
            userId = chatterUserId
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO supstreamerchatters (chatteruserid, mostrecentsup, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET mostrecentsup = EXCLUDED.mostrecentsup
            ''',
            chatterUserId, mostRecentSup.isoformat(), twitchChannelId
        )

        await connection.close()
