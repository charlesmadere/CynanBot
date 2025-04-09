import json
from datetime import datetime
from typing import Any, Collection, Final

from frozenlist import FrozenList
from lru import LRU

from .recentGrenadeAttacksRepositoryInterface import RecentGrenadeAttacksRepositoryInterface
from ..mapper.recentGrenadeAttacksMapperInterface import RecentGrenadeAttacksMapperInterface
from ..models.grenadeAttack import GrenadeAttack
from ..models.recentGrenadeAttackData import RecentGrenadeAttackData
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class RecentGrenadeAttacksRepository(RecentGrenadeAttacksRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        recentGrenadeAttacksMapper: RecentGrenadeAttacksMapperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cacheSize: int = 64
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(recentGrenadeAttacksMapper, RecentGrenadeAttacksMapperInterface):
            raise TypeError(f'recentGrenadeAttacksMapper argument is malformed: \"{recentGrenadeAttacksMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > 256:
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__recentGrenadeAttacksMapper: Final[RecentGrenadeAttacksMapperInterface] = recentGrenadeAttacksMapper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__cache: Final[LRU[str, RecentGrenadeAttackData | None]] = LRU(cacheSize)

    async def add(
        self,
        maximumGrenades: int | None,
        attackedUserId: str,
        attackerUserId: str,
        twitchChannelId: str
    ):
        if maximumGrenades is not None and not utils.isValidInt(maximumGrenades):
            raise TypeError(f'maximumGrenades argument is malformed: \"{maximumGrenades}\"')
        elif maximumGrenades is not None and (maximumGrenades < 1 or maximumGrenades > utils.getIntMaxSafeSize()):
            raise ValueError(f'maximumGrenades argument is out of bounds: {maximumGrenades}')
        elif not utils.isValidStr(attackedUserId):
            raise TypeError(f'attackedUserId argument is malformed: \"{attackedUserId}\"')
        elif not utils.isValidStr(attackerUserId):
            raise TypeError(f'attackerUserId argument is malformed: \"{attackerUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        recentGrenadeAttackData = await self.get(
            attackerUserId = attackerUserId,
            twitchChannelId = twitchChannelId
        )

        newGrenadeAttacks: list[GrenadeAttack] = list(recentGrenadeAttackData.grenadeAttacks)

        newGrenadeAttacks.append(GrenadeAttack(
            attackedDateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            attackedUserId = attackedUserId
        ))

        newGrenadeAttacks.sort(key = lambda entry: entry.attackedDateTime, reverse = True)

        while maximumGrenades is not None and len(newGrenadeAttacks) > maximumGrenades:
            del newGrenadeAttacks[len(newGrenadeAttacks) - 1]

        frozenNewGrenadeAttacks: FrozenList[GrenadeAttack] = FrozenList(newGrenadeAttacks)
        frozenNewGrenadeAttacks.freeze()

        newGrenadeAttacksJsonString = await self.__serializeGrenadeAttacks(
            grenadeAttacks = frozenNewGrenadeAttacks
        )

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO recentgrenadeattacks (attackeruserid, grenadeattacksjson, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (attackeruserid, twitchchannelid) DO UPDATE SET grenadeattacksjson = EXCLUDED.grenadeattacksjson
            ''',
            attackerUserId, newGrenadeAttacksJsonString, twitchChannelId
        )

        await connection.close()

        self.__cache[f'{twitchChannelId}:{attackerUserId}'] = RecentGrenadeAttackData(
            grenadeAttacks = frozenNewGrenadeAttacks,
            attackerUserId = attackerUserId,
            twitchChannelId = twitchChannelId
        )

        self.__timber.log('RecentGrenadeAttacksRepository', f'Added recent grenade attack ({len(frozenNewGrenadeAttacks)=}) ({maximumGrenades=}) ({attackedUserId=}) ({attackerUserId=}) ({twitchChannelId=})')

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('RecentGrenadeAttacksRepository', 'Caches cleared')

    async def get(
        self,
        attackerUserId: str,
        twitchChannelId: str
    ) -> RecentGrenadeAttackData:
        if not utils.isValidStr(attackerUserId):
            raise TypeError(f'attackerUserId argument is malformed: \"{attackerUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedData = self.__cache.get(f'{twitchChannelId}:{attackerUserId}', None)

        if cachedData is not None:
            return cachedData

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT grenadeattacksjson FROM recentgrenadeattacks
                WHERE attackeruserid = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            attackerUserId, twitchChannelId
        )

        await connection.close()
        grenadeAttacksJsonString: str | None = None

        if record is not None and len(record) >= 1:
            grenadeAttacksJsonString = record[0]

        grenadeAttacks = await self.__parseGrenadeAttacks(
            grenadeAttacksJsonString = grenadeAttacksJsonString
        )

        frozenGrenadeAttacks: FrozenList[GrenadeAttack] = FrozenList()

        if grenadeAttacks is not None:
            frozenGrenadeAttacks.extend(grenadeAttacks)

        frozenGrenadeAttacks.freeze()

        recentGrenadeAttackData = RecentGrenadeAttackData(
            grenadeAttacks = frozenGrenadeAttacks,
            attackerUserId = attackerUserId,
            twitchChannelId = twitchChannelId
        )

        self.__cache[f'{twitchChannelId}:{attackerUserId}'] = recentGrenadeAttackData
        return recentGrenadeAttackData

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
                        CREATE TABLE IF NOT EXISTS recentgrenadeattacks (
                            attackeruserid text NOT NULL,
                            grenadeattacksjson jsonb NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (attackeruserid, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS recentgrenadeattacks (
                            attackeruserid TEXT NOT NULL,
                            grenadeattacksjson TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (attackeruserid, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def __parseGrenadeAttacks(
        self,
        grenadeAttacksJsonString: str | Any | None
    ) -> list[GrenadeAttack] | None:
        if not utils.isValidStr(grenadeAttacksJsonString):
            return None

        grenadeAttacksJson: list[dict[str, Any]] | Any | None = json.loads(grenadeAttacksJsonString)

        if not isinstance(grenadeAttacksJson, list) or len(grenadeAttacksJson) == 0:
            return None

        grenadeAttacks: list[GrenadeAttack] = list()

        for grenadeAttackJson in grenadeAttacksJson:
            grenadeAttack = await self.__recentGrenadeAttacksMapper.parseGrenadeAttack(grenadeAttackJson)
            grenadeAttacks.append(grenadeAttack)

        grenadeAttacks.sort(key = lambda entry: entry.attackedDateTime, reverse = True)
        return grenadeAttacks

    async def __serializeGrenadeAttacks(
        self,
        grenadeAttacks: Collection[GrenadeAttack] | None
    ) -> str | None:
        if grenadeAttacks is None:
            return None
        elif not isinstance(grenadeAttacks, Collection):
            raise TypeError(f'grenadeAttacks argument is malformed: \"{grenadeAttacks}\"')

        grenadeAttacksJson: list[dict[str, Any]] = list()

        for grenadeAttack in grenadeAttacks:
            grenadeAttackJson = await self.__recentGrenadeAttacksMapper.serializeGrenadeAttack(grenadeAttack)
            grenadeAttacksJson.append(grenadeAttackJson)

        if len(grenadeAttacksJson) == 0:
            return None

        return json.dumps(grenadeAttacksJson, allow_nan = False, sort_keys = True)
