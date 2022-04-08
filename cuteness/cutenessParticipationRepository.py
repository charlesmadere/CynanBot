from typing import List

import CynanBotCommon.utils as utils
from aiosqlite import Connection
from CynanBotCommon.backingDatabase import BackingDatabase

from cuteness.cutenessDate import CutenessDate


class CutenessParticipationRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        historySize: int = 3
    ):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not utils.isValidNum(historySize):
            raise ValueError(f'historySize argument is malformed: \"{historySize}\"')
        elif historySize < 2 or historySize > 12:
            raise ValueError(f'historySize argument is out of bounds: \"{historySize}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__historySize: int = historySize

        self.__isDatabaseReady: bool = False

    async def getCutenessParticipation(
        self,
        twitchChannel: str,
        userId: str
    ) -> List[CutenessDate]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                SELECT utcYearAndMonth FROM cutenessParticipation
                WHERE twitchChannel = ? AND userId = ?
                LIMIT ?
                ORDER BY utcYearAndMonth DESC
            ''',
            ( twitchChannel, userId, self.__historySize )
        )

        rows = await cursor.fetchmany(size = self.__historySize)

        if len(rows) == 0:
            return None

        cutenessDates: List[CutenessDate] = list()

        for row in rows:
            cutenessDates.append(CutenessDate(row[0]))

        return cutenessDates

    async def __getDatabaseConnection(self) -> Connection:
        await self.__initDatabaseTables()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTables(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True

        connection = await self.__backingDatabase.getConnection()
        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS cutenessParticipation (
                    twitchChannel TEXT NOT NULL COLLATE NOCASE,
                    userId TEXT NOT NULL COLLATE NOCASE,
                    utcYearAndMonth TEXT NOT NULL COLLATE NOCASE,
                    PRIMARY KEY (twitchChannel, userId, utcYearAndMonth)
                )
            '''
        )

        await connection.commit()
        await cursor.close()
        await connection.close()

    async def saveParticipator(
        self,
        cutenessDate: CutenessDate,
        twitchChannel: str,
        userId: str
    ):
        if cutenessDate is None:
            raise ValueError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                INSERT INTO cutenessParticipation (twitchChannel, userId, utcYearAndMonth)
                VALUES (?, ?, ?)
            ''',
            ( twitchChannel, userId, cutenessDate.toStr() )
        )

        await connection.commit()
        await cursor.close()
        await connection.close()
