from backingDatabase import BackingDatabase
import locale
from userIdsRepository import UserIdsRepository

class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        leaderboardSize: int,
        localLeaderboardSize: int,
        userIdsRepository: UserIdsRepository
    ):
        if backingDatabase == None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif leaderboardSize == None:
            raise ValueError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 1 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: \"{leaderboardSize}\"')
        elif localLeaderboardSize == None:
            raise ValueError(f'localLeaderboardSize argument is malformed: \"{localLeaderboardSize}\"')
        elif localLeaderboardSize < 1 or localLeaderboardSize > 6:
            raise ValueError(f'localLeaderboardSize argument is out of bounds: \"{localLeaderboardSize}\"')
        elif userIdsRepository == None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

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

    def fetchCuteness(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )
        row = cursor.fetchone()

        cuteness = 0
        if row != None:
            cuteness = row[0]

        cursor.close()
        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        return cuteness

    def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if incrementAmount == None:
            raise ValueError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

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
        if row != None:
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
        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        return cuteness

    def fetchLeaderboard(self, twitchChannel: str):
        if twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
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
        leaderboard = list()

        if len(rows) == 0:
            return leaderboard

        rank = 1

        for row in rows:
            userName = self.__userIdsRepository.fetchUserName(row[1])
            rankStr = locale.format_string("#%d", rank, grouping = True)
            leaderboard.append(f'{rankStr} {userName} ({row[0]})')
            rank = rank + 1

        cursor.close()
        return leaderboard
