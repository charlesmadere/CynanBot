import traceback
from typing import Final

from .streamElementsUserKeyRepositoryInterface import StreamElementsUserKeyRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class StreamElementsUserKeyRepository(StreamElementsUserKeyRepositoryInterface):

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
        self.__timber.log('StreamElementsUserKeyRepository', f'Caches cleared')

    async def __consumeSeedFile(self):
        seedFileReader = self.__seedFileReader

        if seedFileReader is None:
            return

        self.__seedFileReader = None

        if not await seedFileReader.fileExistsAsync():
            self.__timber.log('StreamElementsUserKeyRepository', f'Seed file (\"{seedFileReader}\") does not exist')
            return

        jsonContents = await seedFileReader.readJsonAsync()
        await seedFileReader.deleteFileAsync()

        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            self.__timber.log('StreamElementsUserKeyRepository', f'Seed file (\"{seedFileReader}\") is empty')
            return

        self.__timber.log('StreamElementsUserKeyRepository', f'Reading in seed file \"{seedFileReader}\"...')

        for twitchChannel, userKey in jsonContents.items():
            try:
                twitchChannelId = await self.__userIdsRepository.requireUserId(twitchChannel)
            except Exception as e:
                self.__timber.log('StreamElementsUserKeyRepository', f'Failed to fetch Twitch channel ID for \"{twitchChannel}\": {e}', e, traceback.format_exc())
                continue

            await self.set(
                userKey = userKey,
                twitchChannelId = twitchChannelId,
            )

        self.__timber.log('StreamElementsUserKeyRepository', f'Finished reading in seed file \"{seedFileReader}\"')

    async def get(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__cache:
            return self.__cache.get(twitchChannelId, None)

        userKey = await self.__readFromDatabase(twitchChannelId = twitchChannelId)
        self.__cache[twitchChannelId] = userKey
        return userKey

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
                        CREATE TABLE IF NOT EXISTS streamelementsuserkeys (
                            userkey text NOT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS streamelementsuserkeys (
                            userkey TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
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
                SELECT userkey FROM streamelementsuserkeys
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId,
        )

        userKey: str | None = None
        if record is not None and len(record) >= 1:
            userKey = record[0]

        await connection.close()
        return userKey

    async def remove(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__cache.pop(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM streamelementsuserkeys
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId,
        )

        await connection.close()
        self.__timber.log('StreamElementsUserKeyRepository', f'Removed Stream Elements user key for \"{twitchChannelId}\"')

    async def set(
        self,
        userKey: str | None,
        twitchChannelId: str,
    ):
        if userKey is not None and not isinstance(userKey, str):
            raise TypeError(f'userKey argument is malformed: \"{userKey}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if utils.isValidStr(userKey):
            await self.__update(
                userKey = userKey,
                twitchChannelId = twitchChannelId,
            )
        else:
            await self.remove(
                twitchChannelId = twitchChannelId,
            )

    async def __update(
        self,
        userKey: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(userKey):
            raise TypeError(f'userKey argument is malformed: \"{userKey}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__cache[twitchChannelId] = userKey

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO streamelementsuserkeys (userkey, twitchchannelid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannelid) DO UPDATE SET userkey = EXCLUDED.userkey
            ''',
            userKey, twitchChannelId,
        )

        await connection.close()
        self.__timber.log('StreamElementsUserKeyRepository', f'Updated Stream Elements user key for \"{twitchChannelId}\"')
