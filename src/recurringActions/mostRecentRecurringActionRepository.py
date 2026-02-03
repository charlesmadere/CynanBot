from datetime import datetime

from .actions.recurringAction import RecurringAction
from .jsonParser.recurringActionsJsonParserInterface import RecurringActionsJsonParserInterface
from .mostRecentRecurringAction import MostRecentRecurringAction
from .mostRecentRecurringActionRepositoryInterface import MostRecentRecurringActionRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..storage.backingDatabase import BackingDatabase
from ..storage.databaseConnection import DatabaseConnection
from ..storage.databaseType import DatabaseType
from ..timber.timberInterface import TimberInterface


class MostRecentRecurringActionRepository(MostRecentRecurringActionRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        recurringActionsJsonParser: RecurringActionsJsonParserInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(recurringActionsJsonParser, RecurringActionsJsonParserInterface):
            raise TypeError(f'recurringActionsJsonParser argument is malformed: \"{recurringActionsJsonParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__recurringActionsJsonParser: RecurringActionsJsonParserInterface = recurringActionsJsonParser
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getMostRecentRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> MostRecentRecurringAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT actiontype, datetime FROM mostrecentrecurringaction
                WHERE twitchchannelid = $1
                LIMIT 1
            ''',
            twitchChannelId,
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        actionType = await self.__recurringActionsJsonParser.requireActionType(record[0])
        dateTime = datetime.fromisoformat(record[1])

        return MostRecentRecurringAction(
            actionType = actionType,
            dateTime = dateTime,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
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
                        CREATE TABLE IF NOT EXISTS mostrecentrecurringaction (
                            actiontype text NOT NULL,
                            datetime text NOT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS mostrecentrecurringaction (
                            actiontype TEXT NOT NULL,
                            datetime TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def setMostRecentRecurringAction(self, action: RecurringAction):
        if not isinstance(action, RecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        actionTypeString = await self.__recurringActionsJsonParser.serializeActionType(action.actionType)
        nowDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO mostrecentrecurringaction (actiontype, datetime, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (twitchchannelid) DO UPDATE SET actiontype = EXCLUDED.actiontype, datetime = EXCLUDED.datetime
            ''',
            actionTypeString, nowDateTime.isoformat(), action.twitchChannelId,
        )

        await connection.close()
        self.__timber.log('MostRecentRecurringActionRepository', f'Updated most recent recurring action ({action=})')
