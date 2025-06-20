import json
from typing import Final

from frozendict import frozendict

from .chatterInventoryRepositoryInterface import ChatterInventoryRepositoryInterface
from ..mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class ChatterInventoryRepository(ChatterInventoryRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__cache: Final[dict[str, ChatterInventoryData | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('ChatterInventoryRepository', 'Caches cleared')

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterInventoryData:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        inventoryData = self.__cache.get(f'{twitchChannelId}:{chatterUserId}', None)
        if inventoryData is not None:
            return inventoryData

        connection = await self.__getDatabaseConnection()
        inventoryData = await self.__get(
            connection = connection,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        await connection.close()
        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = inventoryData
        return inventoryData

    async def __get(
        self,
        connection: DatabaseConnection,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterInventoryData:
        record = await connection.fetchRow(
            '''
                SELECT inventory FROM chatterinventories
                WHERE chatteruserid = $1 and twitchchannelid = $2
                LIMIT 1
            ''',
            chatterUserId, twitchChannelId
        )

        inventoryJson: dict[str, int | None] | None = None

        if record is not None and len(record) >= 1:
            inventoryJson = json.loads(record[0])

        if inventoryJson is None:
            inventoryJson = dict()

        inventory: dict[ChatterItemType, int] = dict()

        for itemType in ChatterItemType:
            itemTypeString = await self.__chatterInventoryMapper.serializeItemType(itemType)
            inventory[itemType] = inventoryJson.get(itemTypeString, 0)

        return ChatterInventoryData(
            inventory = frozendict(inventory),
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

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
                        CREATE TABLE IF NOT EXISTS chatterinventories (
                            chatteruserid text NOT NULL,
                            inventory jsonb DEFAULT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS chatterinventories (
                            chatteruserid TEXT NOT NULL,
                            inventory TEXT DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (chatteruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def update(
        self,
        itemType: ChatterItemType,
        changeAmount: int,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterInventoryData:
        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')
        elif not utils.isValidInt(changeAmount):
            raise TypeError(f'changeAmount argument is malformed: \"{changeAmount}\"')
        elif changeAmount < utils.getIntMinSafeSize() or changeAmount > utils.getIntMaxSafeSize():
            raise ValueError(f'changeAmount argument is out of bounds: {changeAmount}')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        inventoryData = await self.__get(
            connection = connection,
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        newInventory = dict(inventoryData.inventory)
        newInventory[itemType] = changeAmount + newInventory.get(itemType, 0)

        inventoryJson: dict[str, int] = dict()

        for itemType in ChatterItemType:
            itemTypeString = await self.__chatterInventoryMapper.serializeItemType(itemType)
            inventoryJson[itemTypeString] = newInventory.get(itemType, 0)

        inventoryJsonString = json.dumps(inventoryJson, sort_keys = True)

        await connection.execute(
            '''
                INSERT INTO chatterinventories (chatteruserid, inventory, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (chatteruserid, twitchchannelid) DO UPDATE SET inventory = EXCLUDED.inventory
            ''',
            chatterUserId, inventoryJsonString, twitchChannelId
        )

        await connection.close()

        inventoryData = ChatterInventoryData(
            inventory = frozendict(newInventory),
            chatterUserId = chatterUserId,
            twitchChannelId = twitchChannelId
        )

        self.__cache[f'{twitchChannelId}:{chatterUserId}'] = inventoryData
        self.__timber.log('ChatterInventoryRepository', f'Updated inventory ({newInventory=}) ({itemType=}) ({changeAmount=}) ({chatterUserId=}) ({twitchChannelId=})')

        return inventoryData
