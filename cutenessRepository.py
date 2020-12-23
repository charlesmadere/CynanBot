import locale
from typing import List

from backingDatabase import BackingDatabase
from userIdsRepository import UserIdsRepository


class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        leaderboardSize: int,
        localLeaderboardSize: int,
        userIdsRepository: UserIdsRepository
    ):
        if backingDatabase is None:
            raise ValueError(
                f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif leaderboardSize is None:
            raise ValueError(
                f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 1 or leaderboardSize > 10:
            raise ValueError(
                f'leaderboardSize argument is out of bounds: \"{leaderboardSize}\"')
        elif localLeaderboardSize is None:
            raise ValueError(
                f'localLeaderboardSize argument is malformed: \"{localLeaderboardSize}\"')
        elif localLeaderboardSize < 1 or localLeaderboardSize > 6:
            raise ValueError(
                f'localLeaderboardSize argument is out of bounds: \"{localLeaderboardSize}\"')
        elif userIdsRepository is None:
            raise ValueError(
                f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase = backingDatabase
        self.__leaderboardSize = leaderboardSize
        self.__localLeaderboardSize = localLeaderboardSize
        self.__userIdsRepository = userIdsRepository

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

    def fetchCuteness(self, twitchChannel: str, userName: str):
        if twitchChannel is None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(
                f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userName is None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userId = self.__userIdsRepository.fetchUserId(userName=userName)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            (twitchChannel, userId)
        )
        row = cursor.fetchone()

        cuteness = None
        if row is not None:
            cuteness = row[0]

        cursor.close()
        return CutenessResult(
            cuteness=cuteness,
            localLeaderboard=None,
            userId=userId,
            userName=userName
        )

    def fetchCutenessAndLocalLeaderboard(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if twitchChannel is None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(
                f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userId is None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName is None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userIdsRepository.setUser(userId=userId, userName=userName)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            (twitchChannel, userId)
        )
        row = cursor.fetchone()

        if row is None:
            cursor.close()
            return CutenessResult(
                cuteness=0,
                localLeaderboard=None,
                userId=userId,
                userName=userName
            )

        cuteness = row[0]

        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ?
                ORDER BY ABS(? - ABS(cuteness)) ASC
                LIMIT ?
            ''',
            (twitchChannel, userId, cuteness, self.__localLeaderboardSize)
        )

        rows = cursor.fetchmany(size=self.__localLeaderboardSize)

        if len(rows) == 0:
            cursor.close()
            return CutenessResult(
                cuteness=cuteness,
                localLeaderboard=None,
                userId=userId,
                userName=userName
            )

        sortedRows = sorted(rows, key=lambda row: row[0], reverse=True)
        localLeaderboard = list()

        for row in sortedRows:
            # The try-except here is an unfortunate band-aid around an old, since been fixed, bug
            # that would cause us to not always have a person's username persisted in the database
            # alongside their user ID. So for any users that cause this exception to be raised,
            # we'll just ignore them and continue, as there's nothing more we can do to recover.
            #
            # If we were to ever start from scratch with a brand new database, this try-except
            # would be completely extranneous, and could be removed.
            try:
                userName = self.__userIdsRepository.fetchUserName(row[1])
                localLeaderboard.append(LocalLeaderboardEntry(
                    cuteness=row[0],
                    userId=row[1],
                    userName=userName
                ))
            except RuntimeError:
                # Just log the error and continue, there's nothing more we can do to recover.
                print(
                    f'Encountered a user ID that has no username: \"{row[1]}\"')

        cursor.close()
        return CutenessResult(
            cuteness=cuteness,
            localLeaderboard=localLeaderboard,
            userId=userId,
            userName=userName
        )

    def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if incrementAmount is None:
            raise ValueError(
                f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif twitchChannel is None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(
                f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userId is None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName is None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userIdsRepository.setUser(userId=userId, userName=userName)

        connection = self.__backingDatabase.getConnection()
        cursor = connection.cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            (twitchChannel, userId)
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
            (cuteness, twitchChannel, userId)
        )

        connection.commit()
        cursor.close()
        return CutenessResult(
            cuteness=cuteness,
            localLeaderboard=None,
            userId=userId,
            userName=userName
        )

    def fetchLeaderboard(self, twitchChannel: str):
        if twitchChannel is None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(
                f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelUserId = self.__userIdsRepository.fetchUserId(
            userName=twitchChannel)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ?
                ORDER BY cuteness DESC
                LIMIT ?
            ''',
            (twitchChannel, twitchChannelUserId, self.__leaderboardSize)
        )

        rows = cursor.fetchmany(size=self.__leaderboardSize)
        entries = list()

        if len(rows) == 0:
            cursor.close()
            return LeaderboardResult(
                entries=entries
            )

        rank = 1

        for row in rows:
            userName = self.__userIdsRepository.fetchUserName(row[1])
            entries.append(LeaderboardEntry(
                cuteness=row[0],
                rank=rank,
                userId=row[1],
                userName=userName
            ))
            rank = rank + 1

        cursor.close()
        return LeaderboardResult(
            entries=entries
        )


class CutenessResult():

    def __init__(
        self,
        cuteness: int,
        localLeaderboard: List,
        userId: str,
        userName: str
    ):
        if userId is None or len(userId) == 0 or userId.isspace():
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName is None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness = cuteness
        self.__localLeaderboard = localLeaderboard
        self.__userId = userId
        self.__userName = userName

    def getCuteness(self):
        return self.__cuteness

    def getCutenessStr(self):
        return locale.format_string("%d", self.__cuteness, grouping=True)

    def getLocalLeaderboard(self):
        return self.__localLeaderboard

    def getLocalLeaderboardStr(self, delimiter: str = ', '):
        if delimiter is None:
            raise ValueError(
                f'delimiter argument is malformed: \"{delimiter}\"')

        if not self.hasLocalLeaderboard():
            return ''

        strings = list()

        for entry in self.__localLeaderboard:
            strings.append(entry.toStr())

        return delimiter.join(strings)

    def getUserId(self):
        return self.__userId

    def getUserName(self):
        return self.__userName

    def hasCuteness(self):
        return self.__cuteness is not None and self.__cuteness >= 1

    def hasLocalLeaderboard(self):
        return self.__localLeaderboard is not None and len(self.__localLeaderboard) >= 1


class LeaderboardResult():

    def __init__(self, entries: List):
        self.__entries = entries

    def getEntries(self):
        return self.__entries

    def hasEntries(self):
        return self.__entries is not None and len(self.__entries) >= 1

    def toStr(self, delimiter: str = ', '):
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not self.hasEntries():
            return ''

        strings = list()

        for entry in self.__entries:
            strings.append(entry.toStr())

        return delimiter.join(strings)


class LeaderboardEntry():

    def __init__(
        self,
        cuteness: int,
        rank: int,
        userId: str,
        userName: str
    ):
        if cuteness is None:
            raise ValueError(f'cuteness argument is malformed: \"{cuteness}\"')
        elif rank is None:
            raise ValueError(f'rank argument is malformed: \"{rank}\"')
        elif userId is None or len(userId) == 0 or userId.isspace():
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName is None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness = cuteness
        self.__rank = rank
        self.__userId = userId
        self.__userName = userName

    def getCuteness(self):
        return self.__cuteness

    def getCutenessStr(self):
        return locale.format_string("%d", self.__cuteness, grouping=True)

    def getRank(self):
        return self.__rank

    def getRankStr(self):
        return locale.format_string("%d", self.__rank, grouping=True)

    def getUserId(self):
        return self.__userId

    def getUserName(self):
        return self.__userName

    def toStr(self):
        return f'#{self.getRankStr()} {self.__userName} ({self.getCutenessStr()})'


class LocalLeaderboardEntry():

    def __init__(self, cuteness: int, userId: str, userName: str):
        if cuteness is None:
            raise ValueError(f'cuteness argument is malformed: \"{cuteness}\"')
        elif userId is None or len(userId) == 0 or userId.isspace():
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName is None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cuteness = cuteness
        self.__userId = userId
        self.__userName = userName

    def getCuteness(self):
        return self.__cuteness

    def getCutenessStr(self):
        return locale.format_string("%d", self.__cuteness, grouping=True)

    def getUserId(self):
        return self.__userId

    def getUserName(self):
        return self.__userName

    def toStr(self):
        return f'{self.__userName} ({self.getCutenessStr()})'
