from .chatterPreferredTtsRepositoryInterface import ChatterPreferredTtsRepositoryInterface
from ..mapper.chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from ..models.chatterPrefferedTts import ChatterPreferredTts
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class ChatterPreferredTtsRepository(ChatterPreferredTtsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        chatterPreferredTtsJsonMapper: ChatterPreferredTtsJsonMapperInterface,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(chatterPreferredTtsJsonMapper, ChatterPreferredTtsJsonMapperInterface):
            raise TypeError(f'chatterPreferredTtsJsonMapper argument is malformed: \"{chatterPreferredTtsJsonMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__chatterPreferredTtsJsonMapper: ChatterPreferredTtsJsonMapperInterface = chatterPreferredTtsJsonMapper
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False

    async def clearCaches(self):
        pass

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        pass

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
                        CREATE TABLE IF NOT EXISTS chatterpreferredtts (
                            chatteruserid text NOT NULL,
                            configurationjson text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS chatterpreferredtts (
                            chatteruserid TEXT NOT NULL,
                            configurationjson TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts:
        pass
