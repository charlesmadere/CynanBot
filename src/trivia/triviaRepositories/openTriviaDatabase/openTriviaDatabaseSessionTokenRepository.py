from .openTriviaDatabaseSessionTokenRepositoryInterface import OpenTriviaDatabaseSessionTokenRepositoryInterface
from ....misc import utils as utils
from ....storage.backingDatabase import BackingDatabase
from ....storage.databaseConnection import DatabaseConnection
from ....storage.databaseType import DatabaseType
from ....timber.timberInterface import TimberInterface


class OpenTriviaDatabaseSessionTokenRepository(OpenTriviaDatabaseSessionTokenRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, str | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('OpenTriviaDatabaseSessionTokenRepository', 'Caches cleared')

    async def get(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if twitchChannelId in self.__cache:
            return self.__cache.get(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT sessiontoken FROM opentriviadatabasesessiontokens
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId
        )

        await connection.close()
        sessionToken: str | None = None

        if record is not None and len(record) >= 1:
            sessionToken = record[0]

        self.__cache[twitchChannelId] = sessionToken
        return sessionToken

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
                        CREATE TABLE IF NOT EXISTS opentriviadatabasesessiontokens (
                            sessiontoken text DEFAULT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS opentriviadatabasesessiontokens (
                            sessiontoken TEXT DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def remove(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM opentriviadatabasesessiontokens
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)
        self.__timber.log('OpenTriviaDatabaseSessionTokenRepository', f'Session token for \"{twitchChannelId}\" has been removed')

    async def __set(self, sessionToken: str, twitchChannelId: str):
        if not utils.isValidStr(sessionToken):
            raise TypeError(f'sessionToken argument is malformed: \"{sessionToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO opentriviadatabasesessiontokens (sessiontoken, twitchchannelid)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannelid) DO UPDATE SET sessiontoken = EXCLUDED.sessiontoken
            ''',
            sessionToken, twitchChannelId
        )

        await connection.close()
        self.__cache[twitchChannelId] = sessionToken
        self.__timber.log('OpenTriviaDatabaseSessionTokenRepository', f'Session token for \"{twitchChannelId}\" has been set to \"{sessionToken}\"')

    async def update(self, sessionToken: str | None, twitchChannelId: str):
        if sessionToken is not None and not isinstance(sessionToken, str):
            raise TypeError(f'sessionToken argument is malformed: \"{sessionToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if utils.isValidStr(sessionToken):
            await self.__set(sessionToken = sessionToken, twitchChannelId = twitchChannelId)
        else:
            await self.remove(twitchChannelId = twitchChannelId)
