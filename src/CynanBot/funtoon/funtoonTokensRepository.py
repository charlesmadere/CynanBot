import traceback

import CynanBot.misc.utils as utils
from CynanBot.funtoon.exceptions import NoFuntoonTokenException
from CynanBot.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class FuntoonTokensRepository(FuntoonTokensRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        seedFileReader: JsonReaderInterface | None = None
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif seedFileReader is not None and not isinstance(seedFileReader, JsonReaderInterface):
            raise TypeError(f'seedFileReader argument is malformed: \"{seedFileReader}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__seedFileReader: JsonReaderInterface | None = seedFileReader

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, str | None] = dict()

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

        jsonContents: dict[str, str] | None = await seedFileReader.readJsonAsync()
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
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

        self.__timber.log('FuntoonTokensRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getToken(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannel.lower() in self.__cache:
            return self.__cache[twitchChannel.lower()]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT token FROM funtoontokens
                WHERE twitchchannel = $1
                LIMIT 1
            ''',
            twitchChannel
        )

        await connection.close()
        token: str | None = None

        if utils.hasItems(record):
            token = record[0]

        self.__cache[twitchChannel.lower()] = token

        return token

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS funtoontokens (
                        token text DEFAULT NULL,
                        twitchchannel public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS funtoontokens (
                        token TEXT DEFAULT NULL,
                        twitchchannel TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def requireToken(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        token = await self.getToken(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(token):
            raise NoFuntoonTokenException(f'token for twitchChannel \"{twitchChannel}\" is missing/unavailable')

        return token

    async def setToken(
        self,
        token: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if token is not None and not isinstance(token, str):
            raise TypeError(f'token argument is malformed: \"{token}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()

        if utils.isValidStr(token):
            await connection.execute(
                '''
                    INSERT INTO funtoontokens (token, twitchchannel)
                    VALUES ($1, $2)
                    ON CONFLICT (twitchchannel) DO UPDATE SET token = EXCLUDED.token
                ''',
                token, twitchChannel
            )

            self.__cache[twitchChannel.lower()] = token
            self.__timber.log('FuntoonTokensRepository', f'Funtoon token for \"{twitchChannel}\" has been updated (\"{token}\")')
        else:
            await connection.execute(
                '''
                    DELETE FROM funtoontokens
                    WHERE twitchchannel = $1
                ''',
                twitchChannel
            )

            self.__cache[twitchChannel.lower()] = None
            self.__timber.log('FuntoonTokensRepository', f'Funtoon token for \"{twitchChannel}\" has been deleted')

        await connection.close()
