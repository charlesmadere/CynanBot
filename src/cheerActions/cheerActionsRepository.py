from .absCheerAction import AbsCheerAction
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .exceptions import CheerActionAlreadyExistsException, TooManyCheerActionsException
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface


class CheerActionsRepository(CheerActionsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        cheerActionJsonMapper: CheerActionJsonMapperInterface,
        cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(cheerActionJsonMapper, CheerActionJsonMapperInterface):
            raise TypeError(f'cheerActionJsonMapper argument is malformed: \"{cheerActionJsonMapper}\"')
        elif not isinstance(cheerActionSettingsRepository, CheerActionSettingsRepositoryInterface):
            raise TypeError(f'cheerActionSettingsRepository argument is malformed: \"{cheerActionSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__cheerActionJsonMapper: CheerActionJsonMapperInterface = cheerActionJsonMapper
        self.__cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface = cheerActionSettingsRepository
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, list[AbsCheerAction] | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('CheerActionsRepository', 'Caches cleared')

    async def __createCheerAction(
        self,
        isEnabled: bool,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
        actionType: CheerActionType,
        bits: int,
        configurationJson: str | None,
        twitchChannelId: str
    ) -> AbsCheerAction:
        if not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif configurationJson is not None and not isinstance(configurationJson, str):
            raise TypeError(f'configurationJson argument is out of bounds: \"{configurationJson}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        match actionType:
            case CheerActionType.BEAN_CHANCE:
                return await self.__cheerActionJsonMapper.parseBeanChanceCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId
                )

            case CheerActionType.SOUND_ALERT:
                return await self.__cheerActionJsonMapper.parseSoundAlertCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId
                )

            case CheerActionType.TIMEOUT:
                return await self.__cheerActionJsonMapper.parseTimeoutCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId
                )

            case _:
                raise RuntimeError(f'unknown CheerActionType: \"{actionType}\"')

    async def deleteAction(self, bits: int, twitchChannelId: str) -> AbsCheerAction | None:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        action = await self.getAction(
            bits = bits,
            twitchChannelId = twitchChannelId
        )

        if action is None:
            self.__timber.log('CheerActionsRepository', f'Attempted to delete cheer action \"{bits}\" for \"{twitchChannelId}\", but it does not exist in the database')
            return None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM cheeractions
                WHERE bits = $1 AND userid = $2
            ''',
            bits, twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)
        self.__timber.log('CheerActionsRepository', f'Deleted cheer action ({bits=}) ({twitchChannelId=}) ({action=})')

        return action

    async def getAction(self, bits: int, twitchChannelId: str) -> AbsCheerAction | None:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actions = await self.getActions(twitchChannelId = twitchChannelId)

        if actions is None or len(actions) == 0:
            return None

        for action in actions:
            if action.bits == bits:
                return action

        return None

    async def getActions(self, twitchChannelId: str) -> list[AbsCheerAction]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actions: list[AbsCheerAction] | None = self.__cache.get(twitchChannelId, None)

        if actions is not None:
            return actions

        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT isenabled, bits, actiontype, configurationjson, streamstatusrequirement FROM cheeractions
                WHERE twitchchannelid = $1
                ORDER BY bits DESC
            ''',
            twitchChannelId
        )

        await connection.close()
        actions = list()

        if records is not None and len(records) >= 1:
            for record in records:
                isEnabled = utils.numToBool(record[0])
                bits: int = record[1]
                actionType = await self.__cheerActionJsonMapper.requireCheerActionType(record[2])
                configurationJson: str | None = record[3]
                streamStatusRequirement = await self.__cheerActionJsonMapper.requireCheerActionStreamStatusRequirement(record[4])

                cheerAction = await self.__createCheerAction(
                    isEnabled = isEnabled,
                    bits = bits,
                    actionType = actionType,
                    streamStatusRequirement = streamStatusRequirement,
                    configurationJson = configurationJson,
                    twitchChannelId = twitchChannelId
                )

                actions.append(cheerAction)

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
                            isenabled smallint DEFAULT 1 NOT NULL,
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
                            bits INTEGER NOT NULL,
                            isenabled INTEGER DEFAULT 1 NOT NULL,
                            actiontype TEXT NOT NULL,
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

        actions = await self.getActions(twitchChannelId = action.twitchChannelId)
        maximumPerTwitchChannel = await self.__cheerActionSettingsRepository.getMaximumPerTwitchChannel()

        if len(actions) + 1 > maximumPerTwitchChannel:
            raise TooManyCheerActionsException(f'Attempted to add new cheer action for {action.twitchChannelId=} but they already have the maximum number of cheer actions (actions len: {len(actions)}) ({maximumPerTwitchChannel=})')

        existingAction = await self.getAction(
            bits = action.bits,
            twitchChannelId = action.twitchChannelId
        )

        if existingAction is not None:
            raise CheerActionAlreadyExistsException(f'Attempted to add new cheer action for {action.twitchChannelId=} but they already have a cheer action that requires the given bit amount ({action.bits=}) ({action=})')

        isEnabled = utils.numToBool(action.isEnabled)
        actionTypeString = await self.__cheerActionJsonMapper.serializeCheerActionType(action.actionType)
        configurationJson: str | None = await self.__cheerActionJsonMapper.serializeAbsCheerAction(action)
        streamStatusRequirementString = await self.__cheerActionJsonMapper.serializeCheerActionStreamStatusRequirement(action.streamStatusRequirement)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO cheeractions (bits, isenabled, actiontype, configurationjson, streamstatusrequirement, twitchchannelid)
                VALUES ($1, $2, $3, $4, $5, $6)
            ''',
            action.bits, isEnabled, actionTypeString, configurationJson, streamStatusRequirementString, action.twitchChannelId
        )

        await connection.close()
        self.__cache.pop(action.twitchChannelId, None)
        self.__timber.log('CheerActionsRepository', f'Added new cheer action ({action=})')
