from typing import Any

from frozenlist import FrozenList

from .actions.cutenessRecurringAction import CutenessRecurringAction
from .actions.recurringAction import RecurringAction
from .actions.recurringActionType import RecurringActionType
from .actions.superTriviaRecurringAction import SuperTriviaRecurringAction
from .actions.weatherRecurringAction import WeatherRecurringAction
from .actions.wordOfTheDayRecurringAction import WordOfTheDayRecurringAction
from .jsonParser.recurringActionsJsonParserInterface import RecurringActionsJsonParserInterface
from .recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface


class RecurringActionsRepository(RecurringActionsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        recurringActionsJsonParser: RecurringActionsJsonParserInterface,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(recurringActionsJsonParser, RecurringActionsJsonParserInterface):
            raise TypeError(f'recurringActionsJsonParser argument is malformed: \"{recurringActionsJsonParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__recurringActionsJsonParser: RecurringActionsJsonParserInterface = recurringActionsJsonParser
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False

    async def getAllRecurringActions(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[RecurringAction]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        recurringActions: FrozenList[RecurringAction] = FrozenList()

        cuteness = await self.getCutenessRecurringAction(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if cuteness is not None and cuteness.isEnabled:
            recurringActions.append(cuteness)

        superTrivia = await self.getSuperTriviaRecurringAction(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if superTrivia is not None and superTrivia.isEnabled:
            recurringActions.append(superTrivia)

        weather = await self.getWeatherRecurringAction(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if weather is not None and weather.isEnabled:
            recurringActions.append(weather)

        wordOfTheDay = await self.getWordOfTheDayRecurringAction(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if wordOfTheDay is not None and wordOfTheDay.isEnabled:
            recurringActions.append(wordOfTheDay)

        recurringActions.freeze()
        return recurringActions

    async def getCutenessRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CutenessRecurringAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.CUTENESS,
            twitchChannelId = twitchChannelId
        )

        if record is None or len(record) == 0:
            return None

        return await self.__recurringActionsJsonParser.parseCuteness(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __getRecurringAction(
        self,
        actionType: RecurringActionType,
        twitchChannelId: str
    ) -> FrozenList[Any] | None:
        if not isinstance(actionType, RecurringActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        actionTypeString = await self.__recurringActionsJsonParser.serializeActionType(actionType)

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT configurationjson, isenabled, minutesbetween FROM recurringactions
                WHERE actiontype = $1 AND twitchchannelid = $2
                LIMIT 1
            ''',
            actionTypeString, twitchChannelId
        )

        await connection.close()

        if record is not None and len(record) >= 1:
            return record
        else:
            return None

    async def getSuperTriviaRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SuperTriviaRecurringAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.SUPER_TRIVIA,
            twitchChannelId = twitchChannelId
        )

        if record is None or len(record) == 0:
            return None

        return await self.__recurringActionsJsonParser.parseSuperTrivia(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def getWeatherRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WeatherRecurringAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.WEATHER,
            twitchChannelId = twitchChannelId
        )

        if record is None or len(record) == 0:
            return None

        return await self.__recurringActionsJsonParser.parseWeather(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def getWordOfTheDayRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WordOfTheDayRecurringAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.WORD_OF_THE_DAY,
            twitchChannelId = twitchChannelId
        )

        if record is None or len(record) == 0:
            return None

        return await self.__recurringActionsJsonParser.parseWordOfTheDay(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS recurringactions (
                            actiontype text NOT NULL,
                            configurationjson jsonb DEFAULT NULL,
                            isenabled smallint DEFAULT 1 NOT NULL,
                            minutesbetween integer DEFAULT NULL,
                            twitchchannelid text NOT NULL,
                            PRIMARY KEY (actiontype, twitchchannelid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS recurringactions (
                            actiontype TEXT NOT NULL,
                            configurationjson TEXT DEFAULT NULL,
                            isenabled INTEGER DEFAULT 1 NOT NULL,
                            minutesbetween INTEGER DEFAULT NULL,
                            twitchchannelid TEXT NOT NULL,
                            PRIMARY KEY (actiontype, twitchchannelid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def setRecurringAction(self, action: RecurringAction):
        if not isinstance(action, RecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        configurationJson = await self.__recurringActionsJsonParser.toJson(action)

        await self.__setRecurringAction(
            action = action,
            configurationJson = configurationJson
        )

        self.__timber.log('RecurringActionsRepository', f'Updated {action.actionType} action for \"{action.twitchChannel}\"')

    async def __setRecurringAction(
        self,
        action: RecurringAction,
        configurationJson: str
    ):
        if not isinstance(action, RecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(configurationJson):
            raise TypeError(f'configurationJson argument is malformed: \"{configurationJson}\"')

        actionTypeString = await self.__recurringActionsJsonParser.serializeActionType(action.actionType)
        isEnabled = utils.boolToInt(action.isEnabled)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO recurringactions (actiontype, configurationjson, isenabled, minutesbetween, twitchchannelid)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (actiontype, twitchchannelid) DO UPDATE SET configurationjson = EXCLUDED.configurationjson, isenabled = EXCLUDED.isenabled, minutesbetween = EXCLUDED.minutesbetween
            ''',
            actionTypeString, configurationJson, isEnabled, action.minutesBetween, action.twitchChannelId
        )

        await connection.close()
