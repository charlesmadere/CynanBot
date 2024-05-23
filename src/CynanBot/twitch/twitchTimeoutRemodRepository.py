from datetime import datetime, timedelta

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchTimeoutRemodData import TwitchTimeoutRemodData
from CynanBot.twitch.twitchTimeoutRemodRepositoryInterface import \
    TwitchTimeoutRemodRepositoryInterface


class TwitchTimeoutRemodRepository(TwitchTimeoutRemodRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        remodTimeBuffer: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(remodTimeBuffer, timedelta):
            raise TypeError(f'remodTimeBuffer argument is malformed: \"{remodTimeBuffer}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__remodTimeBuffer: timedelta = remodTimeBuffer

        self.__isDatabaseReady: bool = False

    async def add(self, data: TwitchTimeoutRemodData):
        if not isinstance(data, TwitchTimeoutRemodData):
            raise TypeError(f'data argument is malformed: \"{data}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO twitchtimeoutremodactions (broadcasteruserid, remoddatetime, userid)
                VALUES ($1, $2, $3)
                ON CONFLICT (broadcasteruserid, userid) DO UPDATE SET remoddatetime = EXCLUDED.remoddatetime
            ''',
            data.broadcasterUserId, data.remodDateTime.isoformat(), data.userId
        )

        await connection.close()
        self.__timber.log('CheerActionRemodRepository', f'Added remod action ({data=})')

    async def delete(self, broadcasterUserId: str, userId: str):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM twitchtimeoutremodactions
                WHERE broadcasteruserid = $1 AND userid = $2
            ''',
            broadcasterUserId, userId
        )

        await connection.close()
        self.__timber.log('CheerActionRemodRepository', f'Deleted remod action ({broadcasterUserId=}) ({userId=})')

    async def getAll(self) -> list[TwitchTimeoutRemodData]:
        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT twitchtimeoutremodactions.broadcasteruserid, twitchtimeoutremodactions.remoddatetime, twitchtimeoutremodactions.userid, userids.username FROM twitchtimeoutremodactions
                INNER JOIN userids ON twitchtimeoutremodactions.broadcasteruserid = userids.userid
                ORDER BY twitchtimeoutremodactions.remoddatetime ASC
            '''
        )

        await connection.close()
        data: list[TwitchTimeoutRemodData] = list()
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if records is not None and len(records) >= 1:
            for record in records:
                remodDateTime = datetime.fromisoformat(record[1])

                if remodDateTime >= (now + self.__remodTimeBuffer):
                    break

                data.append(TwitchTimeoutRemodData(
                    remodDateTime = remodDateTime,
                    broadcasterUserId = record[0],
                    broadcasterUserName = record[3],
                    userId = record[2]
                ))

        return data

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS twitchtimeoutremodactions (
                        broadcasteruserid text NOT NULL,
                        remoddatetime text NOT NULL,
                        userid text NOT NULL,
                        PRIMARY KEY (broadcasteruserid, userid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS twitchtimeoutremodactions (
                        broadcasteruserid TEXT NOT NULL,
                        remoddatetime TEXT NOT NULL,
                        userid TEXT NOT NULL,
                        PRIMARY KEY (broadcasteruserid, userid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
