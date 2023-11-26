from typing import Any, List, Optional

import misc.utils as utils
from recurringActions.recurringAction import RecurringAction
from recurringActions.recurringActionsJsonParserInterface import \
    RecurringActionsJsonParserInterface
from recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from recurringActions.recurringActionType import RecurringActionType
from recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from recurringActions.weatherRecurringAction import WeatherRecurringAction
from recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction
from storage.backingDatabase import BackingDatabase
from storage.databaseConnection import DatabaseConnection
from storage.databaseType import DatabaseType
from timber.timberInterface import TimberInterface


class RecurringActionsRepository(RecurringActionsRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        recurringActionsJsonParser: RecurringActionsJsonParserInterface,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(recurringActionsJsonParser, RecurringActionsJsonParserInterface):
            raise ValueError(f'recurringActionsJsonParser argument is malformed: \"{recurringActionsJsonParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__recurringActionsJsonParser: RecurringActionsJsonParserInterface = recurringActionsJsonParser
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False

    async def getAllRecurringActions(
        self,
        twitchChannel: str
    ) -> List[RecurringAction]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        recurringActions: List[RecurringAction] = list()

        superTrivia = await self.getSuperTriviaRecurringAction(twitchChannel)
        if superTrivia is not None and superTrivia.isEnabled():
            recurringActions.append(superTrivia)

        weather = await self.getWeatherRecurringAction(twitchChannel)
        if weather is not None and weather.isEnabled():
            recurringActions.append(weather)

        wordOfTheDay = await self.getWordOfTheDayRecurringAction(twitchChannel)
        if wordOfTheDay is not None and wordOfTheDay.isEnabled():
            recurringActions.append(wordOfTheDay)

        return recurringActions

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __getRecurringAction(
        self,
        actionType: RecurringActionType,
        twitchChannel: str
    ) -> Optional[List[Any]]:
        if not isinstance(actionType, RecurringActionType):
            raise ValueError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT configurationjson, isenabled, minutesbetween FROM recurringactions
                WHERE actiontype = $1 AND twitchchannel = $2
                LIMIT 1
            ''',
            actionType.toStr(), twitchChannel
        )

        await connection.close()

        if utils.hasItems(record):
            return record
        else:
            return None

    async def getSuperTriviaRecurringAction(
        self,
        twitchChannel: str
    ) -> Optional[SuperTriviaRecurringAction]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.SUPER_TRIVIA,
            twitchChannel = twitchChannel
        )

        if not utils.hasItems(record):
            return None

        return await self.__recurringActionsJsonParser.parseSuperTrivia(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel
        )

    async def getWeatherRecurringAction(
        self,
        twitchChannel: str
    ) -> Optional[WeatherRecurringAction]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.WEATHER,
            twitchChannel = twitchChannel
        )

        if not utils.hasItems(record):
            return None

        return await self.__recurringActionsJsonParser.parseWeather(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel
        )

    async def getWordOfTheDayRecurringAction(
        self,
        twitchChannel: str
    ) -> Optional[WordOfTheDayRecurringAction]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        record = await self.__getRecurringAction(
            actionType = RecurringActionType.WORD_OF_THE_DAY,
            twitchChannel = twitchChannel
        )

        if not utils.hasItems(record):
            return None

        return await self.__recurringActionsJsonParser.parseWordOfTheDay(
            enabled = utils.numToBool(record[1]),
            minutesBetween = record[2],
            jsonString = record[0],
            twitchChannel = twitchChannel
        )

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS recurringactions (
                        actiontype text NOT NULL,
                        configurationjson text DEFAULT NULL,
                        isenabled smallint DEFAULT 1 NOT NULL,
                        minutesbetween integer DEFAULT NULL,
                        twitchchannel public.citext NOT NULL,
                        PRIMARY KEY (actiontype, twitchchannel)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS recurringactions (
                        actiontype TEXT NOT NULL,
                        configurationjson TEXT DEFAULT NULL,
                        isenabled INTEGER DEFAULT 1 NOT NULL,
                        minutesbetween INTEGER DEFAULT NULL,
                        twitchchannel TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (actiontype, twitchchannel)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def setRecurringAction(self, action: RecurringAction):
        if not isinstance(action, RecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        configurationJson = await self.__recurringActionsJsonParser.toJson(action)

        await self.__setRecurringAction(
            action = action,
            configurationJson = configurationJson
        )

        self.__timber.log('RecurringActionsRepository', f'Updated {action.getActionType()} action for \"{action.getTwitchChannel()}\"')

    async def __setRecurringAction(
        self,
        action: RecurringAction,
        configurationJson: str
    ):
        isEnabled = utils.boolToNum(action.isEnabled())

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO recurringactions (actiontype, configurationjson, isenabled, minutesbetween, twitchchannel)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (actiontype, twitchchannel) DO UPDATE SET configurationjson = EXCLUDED.configurationjson, isenabled = EXCLUDED.isenabled, minutesbetween = EXCLUDED.minutesbetween
            ''',
            action.getActionType().toStr(), configurationJson, isEnabled, action.getMinutesBetween(), action.getTwitchChannel()
        )

        await connection.close()
