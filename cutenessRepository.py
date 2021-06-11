import locale
from typing import List

import CynanBotCommon.utils as utils
from CynanBotCommon.backingDatabase import BackingDatabase
from userIdsRepository import UserIdsRepository


class CutenessLeaderboardEntry():

    def __init__(
        self,
        cuteness: int,
        rank: int,
        userId: str,
        userName: str
    ):
        if not utils.isValidNum(cuteness):
            raise ValueError(f'cuteness argument is malformed: \"{cuteness}\"')
        elif not utils.isValidNum(rank):
            raise ValueError(f'rank argument is malformed: \"{rank}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness: int = cuteness
        self.__rank: int = rank
        self.__userId: str = userId
        self.__userName: str = userName

    def getCuteness(self) -> int:
        return self.__cuteness

    def getCutenessStr(self) -> str:
        return locale.format_string("%d", self.__cuteness, grouping = True)

    def getRank(self) -> int:
        return self.__rank

    def getRankStr(self) -> str:
        return locale.format_string("%d", self.__rank, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def toStr(self) -> str:
        return f'#{self.getRankStr()} {self.__userName} ({self.getCutenessStr()})'


class CutenessLocalLeaderboardEntry():

    def __init__(
        self,
        cuteness: int,
        userId: str,
        userName: str
    ):
        if not utils.isValidNum(cuteness):
            raise ValueError(f'cuteness argument is malformed: \"{cuteness}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness: int = cuteness
        self.__userId: str = userId
        self.__userName: str = userName

    def getCuteness(self) -> int:
        return self.__cuteness

    def getCutenessStr(self) -> str:
        return locale.format_string("%d", self.__cuteness, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def toStr(self) -> str:
        return f'{self.__userName} ({self.getCutenessStr()})'


class CutenessResult():

    def __init__(
        self,
        cuteness: int,
        localLeaderboard: List[CutenessLocalLeaderboardEntry],
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness: int = cuteness
        self.__localLeaderboard: List[CutenessLocalLeaderboardEntry] = localLeaderboard
        self.__userId: str = userId
        self.__userName: str = userName

    def getCuteness(self) -> int:
        return self.__cuteness

    def getCutenessStr(self) -> str:
        return locale.format_string("%d", self.__cuteness, grouping = True)

    def getLocalLeaderboard(self) -> List[CutenessLocalLeaderboardEntry]:
        return self.__localLeaderboard

    def getLocalLeaderboardStr(self, delimiter: str = ', ') -> str:
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not self.hasLocalLeaderboard():
            return ''

        strings = list()

        for entry in self.__localLeaderboard:
            strings.append(entry.toStr())

        return delimiter.join(strings)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def hasCuteness(self) -> bool:
        return utils.isValidNum(self.__cuteness) and self.__cuteness >= 1

    def hasLocalLeaderboard(self) -> bool:
        return utils.hasItems(self.__localLeaderboard)


class CutenessLeaderboardResult():

    def __init__(self, entries: List[CutenessLeaderboardEntry]):
        self.__entries = entries

    def getEntries(self) -> List[CutenessLeaderboardEntry]:
        return self.__entries

    def hasEntries(self) -> bool:
        return utils.hasItems(self.__entries)

    def toStr(self, delimiter: str = ', ') -> str:
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not self.hasEntries():
            return ''

        strings = list()

        for entry in self.__entries:
            strings.append(entry.toStr())

        return delimiter.join(strings)


class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        leaderboardSize: int,
        localLeaderboardSize: int,
        userIdsRepository: UserIdsRepository,
        doubleCutenessTimeSeconds: int = 300
    ):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not utils.isValidNum(leaderboardSize):
            raise ValueError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 1 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: \"{leaderboardSize}\"')
        elif not utils.isValidNum(localLeaderboardSize):
            raise ValueError(f'localLeaderboardSize argument is malformed: \"{localLeaderboardSize}\"')
        elif localLeaderboardSize < 3 or localLeaderboardSize > 6:
            raise ValueError(f'localLeaderboardSize argument is out of bounds: \"{localLeaderboardSize}\"')
        elif userIdsRepository is None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidNum(doubleCutenessTimeSeconds):
            raise ValueError(f'doubleCutenessTimeSeconds argument is malformed: \"{doubleCutenessTimeSeconds}\"')
        elif doubleCutenessTimeSeconds < 30 or doubleCutenessTimeSeconds > 600:
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

    def fetchCuteness(self, twitchChannel: str, userName: str) -> CutenessResult:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userId = self.__userIdsRepository.fetchUserId(userName = userName)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )

        row = cursor.fetchone()

        cuteness = None
        if row is not None:
            cuteness = row[0]

        cursor.close()

        return CutenessResult(
            cuteness = cuteness,
            localLeaderboard = None,
            userId = userId,
            userName = userName
        )

    def fetchCutenessAndLocalLeaderboard(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ) -> CutenessResult:
        if not utils.isValidStr(twitchChannel):
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

        cuteness = row[0]

        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ?
                ORDER BY ABS(? - ABS(cuteness)) ASC
                LIMIT ?
            ''',
            ( twitchChannel, userId, cuteness, self.__localLeaderboardSize )
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

        # sorts cuteness into highest to lowest order
        rows.sort(key = lambda x: x[0], reverse = True)

        localLeaderboard = list()

        for row in rows:
            # The try-except here is an unfortunate band-aid around an old, since been fixed, bug
            # that would cause us to not always have a person's username persisted in the database
            # alongside their user ID. So for any users that cause this exception to be raised,
            # we'll just ignore them and continue, as there's nothing more we can do to recover.
            #
            # If we were to ever start from scratch with a brand new database, this try-except
            # would be completely extranneous, and could be removed.
            try:
                userName = self.__userIdsRepository.fetchUserName(row[1])
                localLeaderboard.append(CutenessLocalLeaderboardEntry(
                    cuteness = row[0],
                    userId = row[1],
                    userName = userName
                ))
            except RuntimeError:
                # Just log the error and continue, there's nothing more we can do to recover.
                print(f'Encountered a user ID that has no username: \"{row[1]}\"')

        cursor.close()

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
        if incrementAmount is None:
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

    def fetchLeaderboard(self, twitchChannel: str) -> CutenessLeaderboardResult:
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
        entries = list()

        if len(rows) == 0:
            cursor.close()
            return CutenessLeaderboardResult(
                entries = entries
            )

        rank = 1

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

        return CutenessLeaderboardResult(
            entries = entries
        )

    def getDoubleCutenessTimeSeconds(self) -> int:
        return self.__doubleCutenessTimeSeconds

    def getDoubleCutenessTimeSecondsStr(self) -> str:
        return locale.format_string("%d", self.__doubleCutenessTimeSeconds, grouping = True)
