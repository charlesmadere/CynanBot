import locale
from typing import List

import CynanBotCommon.utils as utils
from CynanBotCommon.backingDatabase import BackingDatabase
from users.userIdsRepository import UserIdsRepository

from cuteness.cutenessEntry import CutenessEntry
from cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from cuteness.cutenessLeaderboardResult import CutenessLeaderboardResult
from cuteness.cutenessResult import CutenessResult


class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        userIdsRepository: UserIdsRepository,
        doubleCutenessTimeSeconds: int = 300,
        leaderboardSize: int = 10,
        localLeaderboardSize: int = 5
    ):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not utils.isValidNum(leaderboardSize):
            raise ValueError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 1 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: \"{leaderboardSize}\"')
        elif not utils.isValidNum(localLeaderboardSize):
            raise ValueError(f'localLeaderboardSize argument is malformed: \"{localLeaderboardSize}\"')
        elif localLeaderboardSize < 1 or localLeaderboardSize > 5:
            raise ValueError(f'localLeaderboardSize argument is out of bounds: \"{localLeaderboardSize}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(doubleCutenessTimeSeconds):
            raise ValueError(f'doubleCutenessTimeSeconds argument is malformed: \"{doubleCutenessTimeSeconds}\"')
        elif doubleCutenessTimeSeconds < 15 or doubleCutenessTimeSeconds > 300:
            raise ValueError(f'doubleCutenessTimeSeconds argument is out of bounds \"{doubleCutenessTimeSeconds}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__leaderboardSize: int = leaderboardSize
        self.__localLeaderboardSize: int = localLeaderboardSize
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__doubleCutenessTimeSeconds: int = doubleCutenessTimeSeconds

        connection = backingDatabase.getConnection()
        connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS cuteness (
                    cuteness INTEGER NOT NULL DEFAULT 0,
                    twitchChannel TEXT NOT NULL COLLATE NOCASE,
                    userId TEXT NOT NULL COLLATE NOCASE,
                    PRIMARY KEY (twitchChannel, userId)
                )
            '''
        )

        connection.commit()

    def fetchCuteness(
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
        elif not utils.isValidStr(userId) or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )

        row = cursor.fetchone()

        if row is None:
            cursor.close()
            return CutenessResult(
                cuteness = 0,
                localLeaderboard = None,
                userId = userId,
                userName = userName
            )

        cuteness: int = row[0]

        if not fetchLocalLeaderboard:
            cursor.close()
            return CutenessResult(
                cuteness = cuteness,
                localLeaderboard = None,
                userId = userId,
                userName = userName
            )

        twitchChannelUserId = self.__userIdsRepository.fetchUserId(userName = twitchChannel)

        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ? AND userId != ?
                ORDER BY ABS(? - ABS(cuteness)) ASC
                LIMIT ?
            ''',
            ( twitchChannel, userId, twitchChannelUserId, cuteness, self.__localLeaderboardSize )
        )

        rows = cursor.fetchmany(size = self.__localLeaderboardSize)

        if len(rows) == 0:
            cursor.close()
            return CutenessResult(
                cuteness = cuteness,
                localLeaderboard = None,
                userId = userId,
                userName = userName
            )

        localLeaderboard: List[CutenessEntry] = list()

        for row in rows:
            # The try-except here is an unfortunate band-aid around an old, since been fixed, bug
            # that would cause us to not always have a person's username persisted in the database
            # alongside their user ID. So for any users that cause this exception to be raised,
            # we'll just ignore them and continue, as there's nothing more we can do to recover.
            #
            # If we were to ever start from scratch with a brand new database, this try-except
            # would be completely extranneous, and could be removed.
            try:
                entryUserName = self.__userIdsRepository.fetchUserName(row[1])
                localLeaderboard.append(CutenessEntry(
                    cuteness = row[0],
                    userId = row[1],
                    userName = entryUserName
                ))
            except RuntimeError:
                # Just log the error and continue, there's nothing more we can do to recover.
                print(f'Encountered a user ID that has no username: \"{row[1]}\"')

        cursor.close()

        # sorts cuteness into highest to lowest order
        localLeaderboard.sort(key = lambda entry: entry.getCuteness(), reverse = True)

        return CutenessResult(
            cuteness = cuteness,
            localLeaderboard = localLeaderboard,
            userId = userId,
            userName = userName
        )

    def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessResult:
        if not utils.isValidNum(incrementAmount):
            raise ValueError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId) or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        connection = self.__backingDatabase.getConnection()
        cursor = connection.cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )

        row = cursor.fetchone()

        cuteness = 0
        if row is not None:
            cuteness = row[0]

        cuteness = cuteness + incrementAmount

        if cuteness < 0:
            cuteness = 0

        cursor.execute(
            '''
                INSERT INTO cuteness (cuteness, twitchChannel, userId)
                VALUES (?, ?, ?)
                ON CONFLICT (twitchChannel, userId) DO UPDATE SET cuteness = excluded.cuteness
            ''',
            ( cuteness, twitchChannel, userId )
        )

        connection.commit()
        cursor.close()

        return CutenessResult(
            cuteness = cuteness,
            localLeaderboard = None,
            userId = userId,
            userName = userName
        )

    def fetchCutenessLeaderboard(
        self,
        twitchChannel: str,
        specificLookupUserId: str = None,
        specificLookupUserName: str = None
    ) -> CutenessLeaderboardResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelUserId = self.__userIdsRepository.fetchUserId(userName = twitchChannel)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ?
                ORDER BY cuteness DESC
                LIMIT ?
            ''',
            ( twitchChannel, twitchChannelUserId, self.__leaderboardSize )
        )

        rows = cursor.fetchmany(size = self.__leaderboardSize)
        entries: List[CutenessLeaderboardEntry] = list()

        if len(rows) == 0:
            cursor.close()
            return CutenessLeaderboardResult(entries = entries)

        rank: int = 1

        for row in rows:
            userName = self.__userIdsRepository.fetchUserName(row[1])
            entries.append(CutenessLeaderboardEntry(
                cuteness = row[0],
                rank = rank,
                userId = row[1],
                userName = userName
            ))
            rank = rank + 1

        cursor.close()

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
                    specificLookupUserId = self.__userIdsRepository.fetchUserId(userName = specificLookupUserName)
                except ValueError:
                    # this exception can be safely ignored
                    pass
            elif not utils.isValidStr(specificLookupUserName):
                try:
                    specificLookupUserName = self.__userIdsRepository.fetchUserName(specificLookupUserId)
                except (RuntimeError, ValueError):
                    # this exception can be safely ignored
                    pass

            if utils.isValidStr(specificLookupUserId) and utils.isValidStr(specificLookupUserName):
                specificLookupCutenessResult = self.fetchCuteness(
                    fetchLocalLeaderboard = False,
                    twitchChannel = twitchChannel,
                    userId = specificLookupUserId,
                    userName = specificLookupUserName
                )

        return CutenessLeaderboardResult(
            entries = entries,
            specificLookupCutenessResult = specificLookupCutenessResult
        )

    def getDoubleCutenessTimeSeconds(self) -> int:
        return self.__doubleCutenessTimeSeconds

    def getDoubleCutenessTimeSecondsStr(self) -> str:
        return locale.format_string("%d", self.__doubleCutenessTimeSeconds, grouping = True)
