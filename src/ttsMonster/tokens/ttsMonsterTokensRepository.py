import traceback
from typing import Any, Final

from .ttsMonsterTokensRepositoryInterface import TtsMonsterTokensRepositoryInterface
from ..models.ttsMonsterTokens import TtsMonsterTokens
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TtsMonsterTokensRepository(TtsMonsterTokensRepositoryInterface):

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
        self.__cache: Final[dict[str, TtsMonsterTokens | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TtsMonsterTokensRepository', f'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('TtsMonsterTokensRepository', f'Seed file does not exist ({seedFileReader=})')
            return

        jsonContents: dict[str, dict[str, Any]] | None = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('TtsMonsterTokensRepository', f'Seed file is empty ({seedFileReader=})')
            return

        self.__timber.log('TtsMonsterTokensRepository', f'Reading in seed file ({seedFileReader=})...')

        for twitchChannel, tokensJson in jsonContents.items():
            try:
                twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)
            except Exception as e:
                self.__timber.log('TtsMonsterTokensRepository', f'Failed to fetch Twitch channel ID ({twitchChannel=}) ({seedFileReader=})', e, traceback.format_exc())
                continue

            ttsMonsterKey: str | None = None
            if 'key' in tokensJson and utils.isValidStr(tokensJson.get('key')):
                ttsMonsterKey = utils.getStrFromDict(tokensJson, 'key')

            ttsMonsterUserId: str | None = None
            if 'userId' in tokensJson and utils.isValidStr(tokensJson.get('userId')):
                ttsMonsterUserId = utils.getStrFromDict(tokensJson, 'userId')

            await self.set(
                ttsMonsterKey = ttsMonsterKey,
                ttsMonsterUserId = ttsMonsterUserId,
                twitchChannelId = twitchChannelId,
            )

        self.__timber.log('TtsMonsterTokensRepository', f'Finished reading in seed file ({seedFileReader=})')

    async def get(
        self,
        twitchChannelId: str,
    ) -> TtsMonsterTokens | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__cache:
            return self.__cache[twitchChannelId]

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT key, userid FROM ttsmonstertokens
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId,
        )

        await connection.close()
        tokens: TtsMonsterTokens | None = None

        if record is not None and len(record) >= 1:
            tokens = TtsMonsterTokens(
                key = record[0],
                twitchChannelId = twitchChannelId,
                userId = record[1],
            )

        self.__cache[twitchChannelId] = tokens
        return tokens

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
                        CREATE TABLE IF NOT EXISTS ttsmonstertokens (
                            key text NOT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY,
                            userid text NOT NULL
                        )
                    ''',
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS ttsmonstertokens (
                            key TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY,
                            userid TEXT NOT NULL
                        ) STRICT
                    ''',
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()
        await self.__consumeSeedFile()

    async def set(
        self,
        ttsMonsterKey: str | None,
        ttsMonsterUserId: str | None,
        twitchChannelId: str,
    ):
        if ttsMonsterKey is not None and not isinstance(ttsMonsterKey, str):
            raise TypeError(f'ttsMonsterKey argument is malformed: \"{ttsMonsterKey}\"')
        elif ttsMonsterUserId is not None and not isinstance(ttsMonsterUserId, str):
            raise TypeError(f'ttsMonsterUserId argument is malformed: \"{ttsMonsterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()

        if utils.isValidStr(ttsMonsterKey) and utils.isValidStr(ttsMonsterUserId):
            await connection.execute(
                '''
                    INSERT INTO ttsmonstertokens (key, twitchchannelid, userid)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (twitchchannelid) DO UPDATE SET key = EXCLUDED.key, userid = EXCLUDED.userid
                ''',
                ttsMonsterKey, twitchChannelId, ttsMonsterUserId,
            )

            tokens = TtsMonsterTokens(
                key = ttsMonsterKey,
                twitchChannelId = twitchChannelId,
                userId = ttsMonsterUserId,
            )

            self.__cache[twitchChannelId] = tokens
            self.__timber.log('TtsMonsterTokensRepository', f'TTS Monster key and user ID has been updated ({tokens=})')
        else:
            await connection.execute(
                '''
                    DELETE FROM ttsmonstertokens
                    WHERE twitchchannelid = $1
                ''',
                twitchChannelId,
            )

            self.__cache[twitchChannelId] = None
            self.__timber.log('TtsMonsterTokensRepository', f'TTS Monster key and user ID has been deleted ({twitchChannelId=})')

        await connection.close()
