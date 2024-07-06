from .absCheerAction import AbsCheerAction

from .cheerAction import CheerAction
from .cheerActionBitRequirement import CheerActionBitRequirement
from .cheerActionIdGeneratorInterface import CheerActionIdGeneratorInterface
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .exceptions import (CheerActionAlreadyExistsException,
                         TimeoutDurationSecondsTooLongException,
                         TooManyCheerActionsException)
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface


class CheerActionsRepository(CheerActionsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        cheerActionIdGenerator: CheerActionIdGeneratorInterface,
        cheerActionJsonMapper: CheerActionJsonMapperInterface,
        cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface):
            raise TypeError(f'cheerActionIdGenerator argument is malformed: \"{cheerActionIdGenerator}\"')
        elif not isinstance(cheerActionJsonMapper, CheerActionJsonMapperInterface):
            raise TypeError(f'cheerActionJsonMapper argument is malformed: \"{cheerActionJsonMapper}\"')
        elif not isinstance(cheerActionSettingsRepository, CheerActionSettingsRepositoryInterface):
            raise TypeError(f'cheerActionSettingsRepository argument is malformed: \"{cheerActionSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__cheerActionIdGenerator: CheerActionIdGeneratorInterface = cheerActionIdGenerator
        self.__cheerActionJsonMapper: CheerActionJsonMapperInterface = cheerActionJsonMapper
        self.__cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface = cheerActionSettingsRepository
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, list[CheerAction] | None] = dict()

    async def addAction(
        self,
        bitRequirement: CheerActionBitRequirement,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        bits: int,
        durationSeconds: int | None,
        tag: str | None,
        twitchChannelId: str
    ) -> CheerAction:
        if not isinstance(bitRequirement, CheerActionBitRequirement):
            raise TypeError(f'actionRequirement argument is malformed: \"{bitRequirement}\"')
        elif not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise TypeError(f'cheerActionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif durationSeconds is not None and not utils.isValidInt(durationSeconds):
            raise TypeError(f'durationSeconds argument is malformed: \"{durationSeconds}\"')
        elif durationSeconds is not None and durationSeconds < 0:
            raise ValueError(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif durationSeconds is not None and durationSeconds > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'durationSeconds argument is out of bounds: {durationSeconds}')
        elif tag is not None and not isinstance(tag, str):
            raise TypeError(f'tag argument is malformed: \"{tag}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actions = await self.getActions(twitchChannelId)
        maximumPerTwitchChannel = await self.__cheerActionSettingsRepository.getMaximumPerTwitchChannel()

        if len(actions) + 1 > maximumPerTwitchChannel:
            raise TooManyCheerActionsException(f'Attempted to add new cheer action for {twitchChannelId=} but they already have the maximum number of cheer actions (actions len: {len(actions)}) ({maximumPerTwitchChannel=})')

        for action in actions:
            if action.amount == bits:
                raise CheerActionAlreadyExistsException(f'Attempted to add new cheer action for {twitchChannelId=} but they already have a cheer action that requires the given bit amount ({bits=}) ({action=})')

        actionTypeString = await self.__cheerActionJsonMapper.serializeCheerActionType(actionType)
        configurationJson: str | None = None # TODO
        streamStatusRequirementString = await self.__cheerActionJsonMapper.serializeCheerActionStreamStatusRequirement(streamStatusRequirement)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO cheeractions (actiontype, bits, configurationjson, streamstatusrequirement, twitchchannelid)
                VALUES ($1, $2, $3, $4, $5)
            ''',
            actionTypeString, bits, configurationJson, streamStatusRequirementString, twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)

        action = await self.getAction(
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            raise RuntimeError(f'Just finished creating a new action for Twitch channel ID \"{twitchChannelId}\", but it seems to not exist ({bits=}) ({twitchChannelId=})')

        self.__timber.log('CheerActionsRepository', f'Added new cheer action ({action=})')
        return action

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('CheerActionsRepository', 'Caches cleared')

    async def deleteAction(self, bits: int, userId: str) -> CheerAction | None:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        action = await self.getAction(
            bits = bits,
            userId = userId
        )

        if action is None:
            self.__timber.log('CheerActionsRepository', f'Attempted to delete cheer \"{bits}\", but it does not exist in the database')
            return None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM cheeractions
                WHERE bits = $1 AND userid = $2
            ''',
            bits, userId
        )

        await connection.close()
        self.__cache.pop(action.userId, None)
        self.__timber.log('CheerActionsRepository', f'Deleted cheer action ({bits=}) ({userId=}) ({action=})')

        return action

    async def getAction(self, bits: int, twitchChannelId: str) -> CheerAction | None:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actions = await self.getActions(
            twitchChannelId = twitchChannelId
        )

        if actions is None or len(actions) == 0:
            return None

        for action in actions:
            if action.amount == bits:
                return action

        return None

    async def getActions(self, twitchChannelId: str) -> list[CheerAction]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actions: list[CheerAction] | None = self.__cache.get(twitchChannelId, None)

        if actions is not None:
            return actions

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cheeractions.bitrequirement, cheeractions.streamstatusrequirement, cheeractions.actiontype, cheeractions.bits, cheeractions.durationseconds, cheeractions.tag, userids.username FROM cheeractions
                INNER JOIN userids ON cheeractions.twitchchannelid = userids.userid
                WHERE cheeractions.twitchchannelid = $1
                ORDER BY cheeractions.bits DESC
            ''',
            twitchChannelId
        )

        await connection.close()
        actions = list()

        if records is not None and len(records) >= 1:
            for record in records:
                bitRequirement = await self.__cheerActionJsonMapper.requireCheerActionBitRequirement(record[0])
                streamStatusRequirement = await self.__cheerActionJsonMapper.requireCheerActionStreamStatusRequirement(record[1])
                actionType = await self.__cheerActionJsonMapper.requireCheerActionType(record[2])

                actions.append(CheerAction(
                    bitRequirement = bitRequirement,
                    streamStatusRequirement = streamStatusRequirement,
                    actionType = actionType,
                    amount = record[3],
                    durationSeconds = record[4],
                    tag = record[5],
                    twitchChannel = record[6],
                    twitchChannelId = twitchChannelId
                ))

        self.__cache[twitchChannelId] = actions
        return actions

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.getDatabaseType():
            case DatabaseType.POSTGRESQL:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS cheeractions (
                            bits integer NOT NULL,
                            actiontype text NOT NULL,
                            configurationjson text DEFAULT NULL,
                            streamstatusrequirement text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (bits, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS cheeractions (
                            actiontype TEXT NOT NULL,
                            bits INTEGER NOT NULL,
                            configurationjson TEXT DEFAULT NULL,
                            streamstatusrequirement TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (bits, twitchchannelid)
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def setAction(self, action: AbsCheerAction):
        if not isinstance(action, AbsCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        pass
