from datetime import datetime, timezone, tzinfo

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.recurringActions.mostRecentRecurringAction import \
    MostRecentRecurringAction
from CynanBot.recurringActions.mostRecentRecurringActionRepositoryInterface import \
    MostRecentRecurringActionRepositoryInterface
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface


class MostRecentRecurringActionRepository(MostRecentRecurringActionRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZone, timezone):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZone: tzinfo = timeZone

        self.__isDatabaseReady: bool = False

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getMostRecentRecurringAction(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> MostRecentRecurringAction | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT actiontype, datetime FROM mostrecentrecurringaction
                WHERE twitchchannel = $1
                LIMIT 1
            ''',
            twitchChannel
        )

        await connection.close()

        if not utils.hasItems(record):
            return None

        actionType = RecurringActionType.fromStr(record[0])
        simpleDateTime = SimpleDateTime(utils.getDateTimeFromStr(record[1]))

        return MostRecentRecurringAction(
            actionType = actionType,
            dateTime = simpleDateTime,
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
                    CREATE TABLE IF NOT EXISTS mostrecentrecurringaction (
                        actiontype text NOT NULL,
                        datetime text NOT NULL,
                        twitchchannel public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS mostrecentrecurringaction (
                        actiontype TEXT NOT NULL,
                        datetime TEXT NOT NULL,
                        twitchchannel TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def setMostRecentRecurringAction(self, action: RecurringAction):
        if not isinstance(action, RecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        nowDateTime = datetime.now(self.__timeZone)
        nowDateTimeStr = nowDateTime.isoformat()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO mostrecentrecurringaction (actiontype, datetime, twitchchannel)
                VALUES ($1, $2, $3)
                ON CONFLICT (twitchchannel) DO UPDATE SET actiontype = EXCLUDED.actiontype, datetime = EXCLUDED.datetime
            ''',
            action.getActionType().toStr(), nowDateTimeStr, action.getTwitchChannel()
        )

        await connection.close()

        self.__timber.log('MostRecentRecurringActionRepository', f'Updated \"{action.getActionType()}\" for \"{action.getTwitchChannel()}\" ({nowDateTimeStr})')
