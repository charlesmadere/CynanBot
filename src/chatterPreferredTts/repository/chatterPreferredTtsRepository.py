import json

from lru import LRU

from .chatterPreferredTtsRepositoryInterface import ChatterPreferredTtsRepositoryInterface
from ..mapper.chatterPreferredTtsJsonMapperInterface import ChatterPreferredTtsJsonMapperInterface
from ..models.chatterPrefferedTts import ChatterPreferredTts
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface


class ChatterPreferredTtsRepository(ChatterPreferredTtsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        chatterPreferredTtsJsonMapper: ChatterPreferredTtsJsonMapperInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        cacheSize: int = 64
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(chatterPreferredTtsJsonMapper, ChatterPreferredTtsJsonMapperInterface):
            raise TypeError(f'chatterPreferredTtsJsonMapper argument is malformed: \"{chatterPreferredTtsJsonMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > 256:
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__chatterPreferredTtsJsonMapper: ChatterPreferredTtsJsonMapperInterface = chatterPreferredTtsJsonMapper
        self.__timber: TimberInterface = timber
        self.__ttsJsonMapper : TtsJsonMapperInterface = ttsJsonMapper

        self.__isDatabaseReady: bool = False
        self.__cache: LRU[str, ChatterPreferredTts | None] = LRU(cacheSize)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('ChatterPreferredTtsRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if f'{twitchChannelId}:{chatterUserId}' in self.__cache:
            return self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT configurationjson, provider FROM chatterpreferredtts
                WHERE chatteruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        configurationJsonString: str | None = None
        preferredTtsProviderString: str | None = None

        if record is not None and len(record) >= 1:
            configurationJsonString = record[0]
            preferredTtsProviderString = record[1]

        if not utils.isValidStr(configurationJsonString) or not utils.isValidStr(preferredTtsProviderString):
            self.__cache[f'{twitchChannelId}:{chatterUserId}'] = None
            return None

        provider = await self.__ttsJsonMapper.asyncRequireProvider(
            ttsProvider = preferredTtsProviderString
        )

        configurationJson = json.loads(configurationJsonString)

        properties = await self.__chatterPreferredTtsJsonMapper.parseTtsProperties(
            configurationJson = configurationJson,
            provider = provider
        )

        preferredTts = ChatterPreferredTts(
            properties = properties,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = preferredTts
        return preferredTts

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
                        CREATE TABLE IF NOT EXISTS chatterpreferredtts (
                            chatteruserid text NOT NULL,
                            configurationjson jsonb NOT NULL,
                            provider text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS chatterpreferredtts (
                            chatteruserid TEXT NOT NULL,
                            configurationjson TEXT NOT NULL,
                            provider TEXT NOT NULL,
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
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        preferredTts = await self.get(
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        if preferredTts is None:
            return None

        self.__cache.pop(f'{twitchChannelId}:{chatterUserId}')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM chatterpreferredtts
                WHERE chatteruserid = $1 AND twitchchannelid = $2
            ''',
            chatterUserId, twitchChannelId
        )

        await connection.close()
        self.__timber.log('ChatterPreferredTtsRepository', f'Removed preferred TTS ({preferredTts=})')

        return preferredTts

    async def set(self, preferredTts: ChatterPreferredTts):
        if not isinstance(preferredTts, ChatterPreferredTts):
            raise TypeError(f'preferredTts argument is malformed: \"{preferredTts}\"')

        configurationJson = await self.__chatterPreferredTtsJsonMapper.serializeTtsProperties(
            ttsProperties = preferredTts.properties
        )

        configurationJsonString = json.dumps(configurationJson, sort_keys = True)

        preferredTtsProvider = await self.__ttsJsonMapper.asyncSerializeProvider(
            ttsProvider = preferredTts.properties.provider
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO chatterpreferredtts (chatteruserid, configurationjson, provider, twitchchannelid)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET configurationjson = EXCLUDED.configurationjson, provider = EXCLUDED.provider
            ''',
            preferredTts.chatterUserId, configurationJsonString, preferredTtsProvider, preferredTts.twitchChannelId
        )

        await connection.close()
        self.__cache[f'{preferredTts.twitchChannelId}:{preferredTts.chatterUserId}'] = preferredTts
        self.__timber.log('ChatterPreferredTtsRepository', f'Set preferred TTS ({preferredTts=})')
