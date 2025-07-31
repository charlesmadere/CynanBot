import traceback
from typing import Final

from .funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from ..exceptions import NoFuntoonTokenException
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class FuntoonTokensRepository(FuntoonTokensRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        seedFileReader: JsonReaderInterface | None = None,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif seedFileReader is not None and not isinstance(seedFileReader, JsonReaderInterface):
            raise TypeError(f'seedFileReader argument is malformed: \"{seedFileReader}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__seedFileReader: JsonReaderInterface | None = seedFileReader

        self.__isDatabaseReady: bool = False
        self.__cache: Final[dict[str, str | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('FuntoonTokensRepository', 'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('FuntoonTokensRepository', f'Seed file (\"{seedFileReader}\") does not exist')
            return

        jsonContents = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('FuntoonTokensRepository', f'Seed file (\"{seedFileReader}\") is empty')
            return

        self.__timber.log('FuntoonTokensRepository', f'Reading in seed file \"{seedFileReader}\"...')

        for twitchChannel, token in jsonContents.items():
            try:
                twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)
            except Exception as e:
                self.__timber.log('FuntoonTokensRepository', f'Failed to fetch Twitch channel ID for \"{twitchChannel}\": {e}', e, traceback.format_exc())
                continue

            await self.setToken(
                token = token,
                twitchChannelId = twitchChannelId,
            )

        self.__timber.log('FuntoonTokensRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getToken(
        self,
        twitchChannelId: str,
    ) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__cache:
            return self.__cache[twitchChannelId]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT token FROM funtoontokens
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId
        )

        await connection.close()
        token: str | None = None

        if record is not None and len(record) >= 1:
            token = record[0]

        self.__cache[twitchChannelId] = token
        return token

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS funtoontokens (
                            token text DEFAULT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS funtoontokens (
                            token TEXT DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def requireToken(
        self,
        twitchChannelId: str,
    ) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        token = await self.getToken(
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(token):
            raise NoFuntoonTokenException(f'token for twitchChannel \"{twitchChannelId}\" is missing/unavailable')

        return token

    async def setToken(
        self,
        token: str | None,
        twitchChannelId: str,
    ):
        if token is not None and not isinstance(token, str):
            raise TypeError(f'token argument is malformed: \"{token}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()

        if utils.isValidStr(token):
            await connection.execute(
                '''
                    INSERT INTO funtoontokens (token, twitchchannelid)
                    VALUES ($1, $2)
                    ON CONFLICT (twitchchannelid) DO UPDATE SET token = EXCLUDED.token
                ''',
                token, twitchChannelId
            )

            self.__cache[twitchChannelId] = token
            self.__timber.log('FuntoonTokensRepository', f'Funtoon token has been updated ({twitchChannelId=}) ({token=})')
        else:
            await connection.execute(
                '''
                    DELETE FROM funtoontokens
                    WHERE twitchchannelid = $1
                ''',
                twitchChannelId
            )

            self.__cache[twitchChannelId] = None
            self.__timber.log('FuntoonTokensRepository', f'Funtoon token has been deleted ({twitchChannelId=})')

        await connection.close()
