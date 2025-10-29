import traceback
from typing import Final

from frozendict import frozendict

from .absCheerAction import AbsCheerAction
from .cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from .cheerActionType import CheerActionType
from .cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .editCheerActionResult.alreadyDisabledEditCheerActionResult import AlreadyDisabledEditCheerActionResult
from .editCheerActionResult.alreadyEnabledEditCheerActionResult import AlreadyEnabledEditCheerActionResult
from .editCheerActionResult.editCheerActionResult import EditCheerActionResult
from .editCheerActionResult.notFoundEditCheerActionResult import NotFoundEditCheerActionResult
from .editCheerActionResult.successfullyDisabledEditCheerActionResult import SuccessfullyDisabledEditCheerActionResult
from .editCheerActionResult.successfullyEnabledEditCheerActionResult import SuccessfullyEnabledEditCheerActionResult
from .exceptions import CheerActionAlreadyExistsException, TooManyCheerActionsException
from .settings.cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
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
        timber: TimberInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(cheerActionJsonMapper, CheerActionJsonMapperInterface):
            raise TypeError(f'cheerActionJsonMapper argument is malformed: \"{cheerActionJsonMapper}\"')
        elif not isinstance(cheerActionSettingsRepository, CheerActionSettingsRepositoryInterface):
            raise TypeError(f'cheerActionSettingsRepository argument is malformed: \"{cheerActionSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__cheerActionJsonMapper: Final[CheerActionJsonMapperInterface] = cheerActionJsonMapper
        self.__cheerActionSettingsRepository: Final[CheerActionSettingsRepositoryInterface] = cheerActionSettingsRepository
        self.__timber: Final[TimberInterface] = timber

        self.__isDatabaseReady: bool = False
        self.__cache: Final[dict[str, frozendict[int, AbsCheerAction]]] = dict()

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
        twitchChannelId: str,
    ) -> AbsCheerAction:
        if not utils.isValidBool(isEnabled):
            raise TypeError(f'isEnabled argument is malformed: \"{isEnabled}\"')
        elif not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')
        elif not isinstance(actionType, CheerActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif configurationJson is not None and not isinstance(configurationJson, str):
            raise TypeError(f'configurationJson argument is out of bounds: \"{configurationJson}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        match actionType:
            case CheerActionType.ADGE:
                return await self.__cheerActionJsonMapper.requireAdgeCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.AIR_STRIKE:
                return await self.__cheerActionJsonMapper.requireAirStrikeCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.BEAN_CHANCE:
                return await self.__cheerActionJsonMapper.requireBeanChanceCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.CROWD_CONTROL:
                return await self.__cheerActionJsonMapper.requireCrowdControlButtonPressCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.GAME_SHUFFLE:
                return await self.__cheerActionJsonMapper.requireCrowdControlGameShuffleCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.ITEM_USE:
                return await self.__cheerActionJsonMapper.requireItemUseCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.SOUND_ALERT:
                return await self.__cheerActionJsonMapper.requireSoundAlertCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.TIMEOUT:
                return await self.__cheerActionJsonMapper.requireTimeoutCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case CheerActionType.VOICEMAIL:
                return await self.__cheerActionJsonMapper.requireVoicemailCheerAction(
                    isEnabled = isEnabled,
                    streamStatusRequirement = streamStatusRequirement,
                    bits = bits,
                    jsonString = configurationJson,
                    twitchChannelId = twitchChannelId,
                )

            case _:
                raise RuntimeError(f'Unknown CheerActionType: \"{actionType}\"')

    async def deleteAction(self, bits: int, twitchChannelId: str) -> AbsCheerAction | None:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        action = await self.getAction(
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            self.__timber.log('CheerActionsRepository', f'Attempted to delete cheer action \"{bits}\" for \"{twitchChannelId}\", but it does not exist in the database')
            return None

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM cheeractions
                WHERE bits = $1 AND twitchchannelid = $2
            ''',
            bits, twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)
        self.__timber.log('CheerActionsRepository', f'Deleted cheer action ({bits=}) ({twitchChannelId=}) ({action=})')

        return action

    async def disableAction(self, bits: int, twitchChannelId: str) -> EditCheerActionResult:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return await self.__enableOrDisableAction(
            enable = False,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

    async def enableAction(self, bits: int, twitchChannelId: str) -> EditCheerActionResult:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return await self.__enableOrDisableAction(
            enable = True,
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

    async def __enableOrDisableAction(
        self,
        enable: bool,
        bits: int,
        twitchChannelId: str,
    ) -> EditCheerActionResult:
        if not utils.isValidBool(enable):
            raise TypeError(f'enable argument is malformed: \"{enable}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        action = await self.getAction(
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            return NotFoundEditCheerActionResult(
                bits = bits,
                twitchChannelId = twitchChannelId,
            )
        elif enable and action.isEnabled:
            return AlreadyEnabledEditCheerActionResult(action)
        elif not enable and not action.isEnabled:
            return AlreadyDisabledEditCheerActionResult(action)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                UPDATE cheeractions
                SET isenabled = $1
                WHERE bits = $2 AND twitchchannelid = $3
            ''',
            utils.boolToInt(enable), bits, twitchChannelId
        )

        await connection.close()
        self.__cache.pop(twitchChannelId, None)

        action = await self.getAction(
            bits = bits,
            twitchChannelId = twitchChannelId,
        )

        if action is None:
            exception = RuntimeError(f'Updated cheer action {enable=} {bits=} {twitchChannelId=}, but then it was unable to be found?')
            self.__timber.log('CheerActionsRepository', f'Updated cheer action but it was then unable to be found ({enable=}) ({bits=}) ({twitchChannelId=}): {exception}', exception, traceback.format_exc())
            raise exception
        elif enable:
            self.__timber.log('CheerActionsRepository', f'Enabled cheer action ({enable=}) ({bits=}) ({twitchChannelId=})')
            return SuccessfullyEnabledEditCheerActionResult(action)
        else:
            self.__timber.log('CheerActionsRepository', f'Disabled cheer action ({enable=}) ({bits=}) ({twitchChannelId=})')
            return SuccessfullyDisabledEditCheerActionResult(action)

    async def getAction(self, bits: int, twitchChannelId: str) -> AbsCheerAction | None:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actions = await self.getActions(twitchChannelId = twitchChannelId)

        if actions is None:
            return None
        else:
            return actions.get(bits, None)

    async def getActions(self, twitchChannelId: str) -> frozendict[int, AbsCheerAction]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedActions = self.__cache.get(twitchChannelId, None)

        if cachedActions is not None:
            return cachedActions

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
        actions: dict[int, AbsCheerAction] = dict()

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
                    twitchChannelId = twitchChannelId,
                )

                actions[bits] = cheerAction

        frozenActions: frozendict[int, AbsCheerAction] = frozendict(actions)
        self.__cache[twitchChannelId] = frozenActions
        return frozenActions

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
                        CREATE TABLE IF NOT EXISTS cheeractions (
                            bits integer NOT NULL,
                            isenabled smallint DEFAULT 1 NOT NULL,
                            actiontype text NOT NULL,
                            configurationjson jsonb DEFAULT NULL,
                            streamstatusrequirement text NOT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (bits, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS cheeractions (
                            bits INTEGER NOT NULL,
                            isenabled INTEGER DEFAULT 1 NOT NULL,
                            actiontype TEXT NOT NULL,
                            configurationjson TEXT DEFAULT NULL,
                            streamstatusrequirement TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (bits, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

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
            twitchChannelId = action.twitchChannelId,
        )

        if existingAction is not None:
            raise CheerActionAlreadyExistsException(f'Attempted to add new cheer action for {action.twitchChannelId=} but they already have a cheer action that requires the given bit amount ({existingAction=}) ({action=})')

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
