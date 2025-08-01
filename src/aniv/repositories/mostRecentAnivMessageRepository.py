from datetime import datetime
from typing import Final

from .mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class MostRecentAnivMessageRepository(MostRecentAnivMessageRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

        self.__isDatabaseReady: bool = False
        self.__cache: dict[str, MostRecentAnivMessage | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('MostRecentAnivMessageRepository', 'Caches cleared')

    async def __deleteMessage(
        self,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__cache.pop(twitchChannelId, None)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM mostrecentanivmessages
                WHERE twitchchannelid = $1
            ''',
            twitchChannelId
        )

        await connection.close()

    async def get(
        self,
        twitchChannelId: str,
    ) -> MostRecentAnivMessage | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        message: MostRecentAnivMessage | None

        if twitchChannelId in self.__cache:
            message = self.__cache.get(twitchChannelId, None)
        else:
            message = await self.__getFromDatabase(
                twitchChannelId = twitchChannelId,
            )

            self.__cache[twitchChannelId] = message

        return message

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __getFromDatabase(
        self,
        twitchChannelId: str,
    ) -> MostRecentAnivMessage | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT datetime, message FROM mostrecentanivmessages
                WHERE twitchchannelid = $1
                LIMIT 1
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
                message = message,
            )
        else:
            return None

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS mostrecentanivmessages (
                            datetime text NOT NULL,
                            message public.citext DEFAULT NULL,
                            twitchchannelid text NOT NULL PRIMARY KEY
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS mostrecentanivmessages (
                            datetime TEXT NOT NULL,
                            message TEXT DEFAULT NULL COLLATE NOCASE,
                            twitchchannelid TEXT NOT NULL PRIMARY KEY
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

    async def __saveMessage(
        self,
        message: str,
        twitchChannelId: str,
    ):
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        anivMessage = MostRecentAnivMessage(
            dateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            message = message,
        )

        self.__cache[twitchChannelId] = anivMessage

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO mostrecentanivmessages (datetime, message, twitchchannelid)
                VALUES ($1, $2, $3)
                ON CONFLICT (twitchchannelid) DO UPDATE SET datetime = EXCLUDED.datetime, message = EXCLUDED.message
            ''',
            anivMessage.dateTime.isoformat(), message, twitchChannelId
        )

        await connection.close()

    async def set(
        self,
        message: str | None,
        twitchChannelId: str,
    ):
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        message = utils.cleanStr(message)

        if utils.isValidStr(message):
            await self.__saveMessage(
                message = message,
                twitchChannelId = twitchChannelId,
            )

            self.__timber.log('MostRecentAnivMessageRepository', f'Updated most recent aniv message in \"{twitchChannelId}\"')
        else:
            await self.__deleteMessage(
                twitchChannelId = twitchChannelId,
            )

            self.__timber.log('MostRecentAnivMessageRepository', f'Removed most recent aniv message in \"{twitchChannelId}\"')
