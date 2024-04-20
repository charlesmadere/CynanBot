from datetime import datetime, timedelta, timezone, tzinfo

import CynanBot.misc.utils as utils
from CynanBot.aniv.mostRecentAnivMessage import MostRecentAnivMessage
from CynanBot.aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface


class MostRecentAnivMessageRepository(MostRecentAnivMessageRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        maxMessageAge: timedelta = timedelta(minutes = 2, seconds = 30),
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(maxMessageAge, timedelta):
            raise TypeError(f'maxMessageAge argument is malformed: \"{maxMessageAge}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__maxMessageAge: timedelta = maxMessageAge
        self.__timeZone: tzinfo = timeZone

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, MostRecentAnivMessage | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('MostRecentAnivMessageRepository', 'Caches cleared')

    async def __deleteMessage(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM mostrecentanivmessages
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId
        )

        await connection.close()

    async def get(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        anivMessage = self.__cache.get(twitchChannelId, None)

        if anivMessage is None:
            anivMessage = await self.__getFromDatabase(twitchChannelId = twitchChannelId)
            self.__cache[twitchChannelId] = anivMessage

        now = datetime.now(self.__timeZone)

        if anivMessage is not None and anivMessage.dateTime + self.__maxMessageAge >= now:
            return anivMessage.message
        else:
            return None

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __getFromDatabase(self, twitchChannelId: str) -> MostRecentAnivMessage | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime, message FROM mostrecentanivmessages
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId
        )

        dateTime: datetime | None = None
        message: str | None = None

        if record is not None and len(record) >= 1:
            dateTime = datetime.fromisoformat(record[0])
            message = record[1]

        await connection.close()

        if dateTime is not None and utils.isValidStr(message):
            return MostRecentAnivMessage(
                dateTime = dateTime,
                message = message
            )
        else:
            return None

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS mostrecentanivmessages (
                        datetime text NOT NULL,
                        message public.citext DEFAULT NULL,
                        twitchchannelid text NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS mostrecentanivmessages (
                        datetime TEXT NOT NULL,
                        message TEXT DEFAULT NULL COLLATE NOCASE,f
                        twitchchannelid TEXT NOT NULL PRIMARY KEY
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

    async def __saveMessage(self, message: str, twitchChannelId: str):
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        nowDateTime = datetime.now(self.__timeZone)
        nowDateTimeStr = nowDateTime.isoformat()

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO mostrecentanivmessages (datetime, message, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (twitchchannelid) DO UPDATE SET datetime = EXCLUDED.datetime, message = EXCLUDED.message
            ''',
            nowDateTimeStr, message, twitchChannelId
        )

        await connection.close()

    async def set(self, message: str | None, twitchChannelId: str):
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if message is not None:
            message = utils.cleanStr(message)

        if utils.isValidStr(message):
            await self.__saveMessage(
                message = message,
                twitchChannelId = twitchChannelId
            )
        else:
            await self.__deleteMessage(twitchChannelId = twitchChannelId)

        self.__timber.log('MostRecentAnivMessageRepository', f'Updated most recent aniv message in \"{twitchChannelId}\"')
