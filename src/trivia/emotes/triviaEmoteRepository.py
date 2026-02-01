from typing import Final

from .triviaEmoteRepositoryInterface import TriviaEmoteRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType


class TriviaEmoteRepository(TriviaEmoteRepositoryInterface):

    def __init__(self, backingDatabase: BackingDatabase):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getEmoteIndexFor(self, twitchChannelId: str) -> int | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT emoteindex FROM triviaemotes
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId,
        )

        emoteIndex: int | None = None

        if record is not None and len(record) >= 1:
            emoteIndex = record[0]

        await connection.close()
        return emoteIndex

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviaemotes (
                            emoteindex smallint DEFAULT 0 NOT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS triviaemotes (
                            emoteindex INTEGER NOT NULL DEFAULT 0,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def setEmoteIndexFor(self, emoteIndex: int, twitchChannelId: str):
        if not utils.isValidInt(emoteIndex):
            raise TypeError(f'emoteIndex argument is malformed: \"{emoteIndex}\"')
        elif emoteIndex < 0 or emoteIndex > utils.getIntMaxSafeSize():
            raise ValueError(f'emoteIndex argument is out of bounds: {emoteIndex}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO triviaemotes (emoteindex, twitchchannelid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannelid) DO UPDATE SET emoteindex = EXCLUDED.emoteindex
            ''',
            emoteIndex, twitchChannelId,
        )

        await connection.close()
