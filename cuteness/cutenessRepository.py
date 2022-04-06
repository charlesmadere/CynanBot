from typing import List, Optional

import CynanBotCommon.utils as utils
from aiosqlite import Connection
from CynanBotCommon.backingDatabase import BackingDatabase
from users.userIdsRepository import UserIdsRepository

from cuteness.cutenessDate import CutenessDate
from cuteness.cutenessEntry import CutenessEntry
from cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult
from cuteness.cutenessResult import CutenessResult


class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        userIdsRepository: UserIdsRepository,
        leaderboardSize: int = 10,
        localLeaderboardSize: int = 5
    ):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(leaderboardSize):
            raise ValueError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 3 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: \"{leaderboardSize}\"')
        elif not utils.isValidNum(localLeaderboardSize):
            raise ValueError(f'localLeaderboardSize argument is malformed: \"{localLeaderboardSize}\"')
        elif localLeaderboardSize < 1 or localLeaderboardSize > 5:
            raise ValueError(f'localLeaderboardSize argument is out of bounds: \"{localLeaderboardSize}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__leaderboardSize: int = leaderboardSize
        self.__localLeaderboardSize: int = localLeaderboardSize

        self.__isDatabaseReady: bool = False

    async def fetchCuteness(
        self,
        fetchLocalLeaderboard: bool,
        twitchChannel: str,
        userId: str,
        userName: str,
    ) -> CutenessResult:
        if not utils.isValidBool(fetchLocalLeaderboard):
            raise ValueError(f'fetchLocalLeaderboard argument is malformed: \"{fetchLocalLeaderboard}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        await self.__userIdsRepository.setUser(userId = userId, userName = userName)

        cutenessDate = CutenessDate()
        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                SELECT cuteness.cuteness, cuteness.userId, userIds.userName FROM cuteness
                INNER JOIN userIds ON cuteness.userId = userIds.userId
                WHERE cuteness.twitchChannel = ? AND cuteness.userId = ? AND cuteness.utcYearAndMonth = ?
            ''',
            ( twitchChannel, userId, cutenessDate.getStr() )
        )

        row = await cursor.fetchone()

        if row is None:
            await cursor.close()
            await connection.close()
            return CutenessResult(
                cutenessDate = cutenessDate,
                cuteness = 0,
                localLeaderboard = None,
                userId = userId,
                userName = userName
            )

        cuteness: int = row[0]

        if not fetchLocalLeaderboard:
            await cursor.close()
            await connection.close()
            return CutenessResult(
                cutenessDate = cutenessDate,
                cuteness = cuteness,
                localLeaderboard = None,
                userId = userId,
                userName = userName
            )

        twitchChannelUserId = await self.__userIdsRepository.fetchUserId(userName = twitchChannel)

        await cursor.execute(
            '''
                SELECT cuteness.cuteness, cuteness.userId, userIds.userName FROM cuteness
                INNER JOIN userIds ON cuteness.userId = userIds.userId
                WHERE cuteness.twitchChannel = ? AND cuteness.utcYearAndMonth = ? AND cuteness.cuteness IS NOT NULL AND cuteness.cuteness >= 1 AND cuteness.userId != ? AND cuteness.userId != ?
                ORDER BY ABS(? - ABS(cuteness.cuteness)) ASC
                LIMIT ?
            ''',
            ( twitchChannel, cutenessDate.getStr(), userId, twitchChannelUserId, cuteness, self.__localLeaderboardSize )
        )

        rows = await cursor.fetchmany(size = self.__localLeaderboardSize)

        if len(rows) == 0:
            await cursor.close()
            await connection.close()
            return CutenessResult(
                cutenessDate = cutenessDate,
                cuteness = cuteness,
                localLeaderboard = None,
                userId = userId,
                userName = userName
            )

        localLeaderboard: List[CutenessEntry] = list()

        for row in rows:
            localLeaderboard.append(CutenessEntry(
                cuteness = row[0],
                userId = row[1],
                userName = row[2]
            ))

        await cursor.close()
        await connection.close()

        # sorts cuteness into highest to lowest order
        localLeaderboard.sort(key = lambda entry: entry.getCuteness(), reverse = True)

        return CutenessResult(
            cutenessDate = cutenessDate,
            cuteness = cuteness,
            localLeaderboard = localLeaderboard,
            userId = userId,
            userName = userName
        )

    async def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessResult:
        if not utils.isValidNum(incrementAmount):
            raise ValueError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif incrementAmount >= utils.getLongMaxSafeSize():
            raise ValueError(f'incrementAmount ({incrementAmount}) is >= maximum value ({utils.getLongMaxSafeSize()})')
        elif incrementAmount <= utils.getLongMinSafeSize():
            raise ValueError(f'incrementAmount ({incrementAmount}) is <= minimum value ({utils.getLongMinSafeSize()})')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        await self.__userIdsRepository.setUser(userId = userId, userName = userName)

        cutenessDate = CutenessDate()
        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ? AND utcYearAndMonth = ?
            ''',
            ( twitchChannel, userId, cutenessDate.getStr() )
        )

        row = await cursor.fetchone()
        oldCuteness: int = 0

        if row is not None:
            oldCuteness = row[0]

        newCuteness: int = oldCuteness + incrementAmount

        if newCuteness < 0:
            newCuteness = 0
        elif newCuteness > utils.getLongMaxSafeSize():
            raise OverflowError(f'New cuteness ({newCuteness}) would be too large (old cuteness = {oldCuteness}) (increment amount = {incrementAmount})')

        await cursor.execute(
            '''
                INSERT INTO cuteness (cuteness, twitchChannel, userId, utcYearAndMonth)
                VALUES (?, ?, ?, ?)
                ON CONFLICT (twitchChannel, userId, utcYearAndMonth) DO UPDATE SET cuteness = excluded.cuteness
            ''',
            ( newCuteness, twitchChannel, userId, cutenessDate.getStr() )
        )

        await connection.commit()
        await cursor.close()
        await connection.close()

        return CutenessResult(
            cutenessDate = cutenessDate,
            cuteness = newCuteness,
            localLeaderboard = None,
            userId = userId,
            userName = userName
        )

    async def fetchCutenessLeaderboard(
        self,
        twitchChannel: str,
        specificLookupUserId: Optional[str] = None,
        specificLookupUserName: Optional[str] = None
    ) -> CutenessLeaderboardResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelUserId = await self.__userIdsRepository.fetchUserId(userName = twitchChannel)

        cutenessDate = CutenessDate()
        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                SELECT cuteness.cuteness, cuteness.userId, userIds.userName FROM cuteness
                INNER JOIN userIds ON cuteness.userId = userIds.userId
                WHERE cuteness.twitchChannel = ? AND cuteness.utcYearAndMonth = ? AND cuteness.cuteness IS NOT NULL AND cuteness.cuteness >= 1 AND cuteness.userId != ?
                ORDER BY cuteness.cuteness DESC
                LIMIT ?
            ''',
            ( twitchChannel, cutenessDate.getStr(), twitchChannelUserId, self.__leaderboardSize )
        )

        rows = await cursor.fetchmany(size = self.__leaderboardSize)

        if len(rows) == 0:
            await cursor.close()
            return CutenessLeaderboardResult(cutenessDate = cutenessDate)

        entries: List[CutenessLeaderboardEntry] = list()
        rank: int = 1

        for row in rows:
            entries.append(CutenessLeaderboardEntry(
                cuteness = row[0],
                rank = rank,
                userId = row[1],
                userName = row[2]
            ))
            rank = rank + 1

        await cursor.close()
        await connection.close()

        # sort cuteness into highest to lowest order
        entries.sort(key = lambda entry: entry.getCuteness(), reverse = True)

        specificLookupAlreadyInResults: bool = False
        if utils.isValidStr(specificLookupUserId) or utils.isValidStr(specificLookupUserName):
            for entry in entries:
                if utils.isValidStr(specificLookupUserId) and entry.getUserId().lower() == specificLookupUserId.lower():
                    specificLookupAlreadyInResults = True
                    break
                elif utils.isValidStr(specificLookupUserName) and entry.getUserName().lower() == specificLookupUserName.lower():
                    specificLookupAlreadyInResults = True
                    break

        specificLookupCutenessResult: CutenessResult = None
        if not specificLookupAlreadyInResults and (utils.isValidStr(specificLookupUserId) or utils.isValidStr(specificLookupUserName)):
            if not utils.isValidStr(specificLookupUserId):
                try:
                    specificLookupUserId = await self.__userIdsRepository.fetchUserId(userName = specificLookupUserName)
                except ValueError:
                    # this exception can be safely ignored
                    pass
            else:
                try:
                    specificLookupUserName = await self.__userIdsRepository.fetchUserName(specificLookupUserId)
                except (RuntimeError, ValueError):
                    # this exception can be safely ignored
                    pass

            if utils.isValidStr(specificLookupUserId) and utils.isValidStr(specificLookupUserName):
                specificLookupCutenessResult = await self.fetchCuteness(
                    fetchLocalLeaderboard = False,
                    twitchChannel = twitchChannel,
                    userId = specificLookupUserId,
                    userName = specificLookupUserName
                )

        return CutenessLeaderboardResult(
            cutenessDate = cutenessDate,
            entries = entries,
            specificLookupCutenessResult = specificLookupCutenessResult
        )

    async def __getDatabaseConnection(self) -> Connection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True

        connection = await self.__backingDatabase.getConnection()
        cursor = await connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS cuteness (
                    cuteness INTEGER NOT NULL DEFAULT 0,
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
