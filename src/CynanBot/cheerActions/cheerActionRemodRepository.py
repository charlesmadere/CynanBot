from datetime import timedelta
from typing import List

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionRemodData import CheerActionRemodData
from CynanBot.cheerActions.cheerActionRemodRepositoryInterface import \
    CheerActionRemodRepositoryInterface
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface


class CheerActionRemodRepository(CheerActionRemodRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        remodTimeBuffer: timedelta = timedelta(seconds = 2)
    ):
        assert isinstance(backingDatabase, BackingDatabase), f"malformed {backingDatabase=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(remodTimeBuffer, timedelta), f"malformed {remodTimeBuffer=}"

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__remodTimeBuffer: timedelta = remodTimeBuffer

        self.__isDatabaseReady: bool = False

    async def add(self, data: CheerActionRemodData):
        assert isinstance(data, CheerActionRemodData), f"malformed {data=}"

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO cheerremodactions (broadcasteruserid, remoddatetime, userid)
                VALUES ($1, $2, $3)
            ''',
            data.getBroadcasterUserId(), data.getRemodDateTime().getIsoFormatStr(), data.getUserId()
        )

        await connection.close()
        self.__timber.log('CheerActionRemodRepository', f'Added remod action ({data=})')

    async def delete(self, broadcasterUserId: str, userId: str):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                DELETE FROM cheerremodactions
                WHERE broadcasteruserid = $1 AND userid = $2
            ''',
            broadcasterUserId, userId
        )

        await connection.close()
        self.__timber.log('CheerActionRemodRepository', f'Deleted remod action ({broadcasterUserId=}) ({userId=})')

    async def getAll(self) -> List[CheerActionRemodData]:
        connection = await self.__getDatabaseConnection()
        records = await connection.fetchRows(
            '''
                SELECT cheerremodactions.broadcasteruserid, cheerremodactions.remoddatetime, cheerremodactions.userid, userids.username FROM cheerremodactions
                INNER JOIN userids ON cheerremodactions.userid = userids.userid
                ORDER BY cheerremodactions.remoddatetime ASC
            '''
        )

        await connection.close()
        data: List[CheerActionRemodData] = list()
        now = SimpleDateTime()

        if utils.hasItems(records):
            for record in records:
                remodDateTime = SimpleDateTime(utils.getDateTimeFromStr(record[1]))

                if remodDateTime >= (now + self.__remodTimeBuffer):
                    break

                data.append(CheerActionRemodData(
                    remodDateTime = remodDateTime,
                    broadcasterUserId = record[0],
                    broadcasterUserName = record[2],
                    userId = record[1]
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
                    CREATE TABLE IF NOT EXISTS cheerremodactions (
                        broadcasteruserid public.citext NOT NULL,
                        remoddatetime text NOT NULL,
                        userid public.citext NOT NULL,
                        PRIMARY KEY (broadcasteruserid, userid)
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS cheerremodactions (
                        broadcasteruserid TEXT NOT NULL COLLATE NOCASE,
                        remoddatetime TEXT NOT NULL,
                        userid TEXT NOT NULL COLLATE NOCASE,
                        PRIMARY KEY (broadcasteruserid, userid)
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
