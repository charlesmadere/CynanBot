import traceback

from .ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TtsMonsterApiTokensRepository(TtsMonsterApiTokensRepositoryInterface):

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
        self.__timber.log('TtsMonsterApiTokensRepository', f'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('TtsMonsterApiTokensRepository', f'Seed file (\"{seedFileReader}\") does not exist')
            return

        jsonContents: dict[str, str] | None = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('TtsMonsterApiTokensRepository', f'Seed file (\"{seedFileReader}\") is empty')
            return

        self.__timber.log('TtsMonsterApiTokensRepository', f'Reading in seed file \"{seedFileReader}\"...')

        for twitchChannel, apiToken in jsonContents.items():
            try:
                twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)
            except Exception as e:
                self.__timber.log('TtsMonsterApiTokensRepository', f'Failed to fetch Twitch channel ID for \"{twitchChannel}\": {e}', e, traceback.format_exc())
                continue

            await self.set(
                apiToken = apiToken,
                twitchChannelId = twitchChannelId
            )

        self.__timber.log('TtsMonsterApiTokensRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def get(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__cache:
            return self.__cache.get(twitchChannelId, None)

        apiToken = await self.__readFromDatabase(twitchChannelId = twitchChannelId)
        self.__cache[twitchChannelId] = apiToken
        return apiToken

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
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS ttsmonsterapitokens (
                            apitoken text NOT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS ttsmonsterapitokens (
                            apitoken TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def __readFromDatabase(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT apitoken FROM ttsmonsterapitokens
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId
        )

        apiToken: str | None = None
        if record is not None and len(record) >= 1:
            apiToken = record[0]

        await connection.close()
        return apiToken

    async def __remove(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__cache.pop(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM ttsmonsterapitokens
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId
        )

        await connection.close()

    async def set(self, apiToken: str | None, twitchChannelId: str):
        if apiToken is not None and not isinstance(apiToken, str):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if utils.isValidStr(apiToken):
            await self.__update(
                apiToken = apiToken,
                twitchChannelId = twitchChannelId
            )

            self.__timber.log('TtsMonsterApiTokensRepository', f'Updated TTS Monster API token for \"{twitchChannelId}\"')
        else:
            await self.__remove(twitchChannelId = twitchChannelId)
            self.__timber.log('TtsMonsterApiTokensRepository', f'Removed TTS Monster API token for \"{twitchChannelId}\"')

    async def __update(self, apiToken: str, twitchChannelId: str):
        if not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__cache[twitchChannelId] = apiToken

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO ttsmonsterapitokens (apitoken, twitchchannelid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannelid) DO UPDATE SET apitoken = EXCLUDED.apitoken
            ''',
            apiToken, twitchChannelId
        )

        await connection.close()
