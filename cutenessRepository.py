from backingDatabase import BackingDatabase
import sqlite3
from userIdsRepository import UserIdsRepository

class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        userIdsRepository: UserIdsRepository
    ):
        if backingDatabase == None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif userIdsRepository == None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase = backingDatabase
        self.__userIdsRepository = userIdsRepository

        connection = backingDatabase.getConnection()
        connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS cuteness (
                    cuteness INTEGER NOT NULL DEFAULT 0,
                    userId TEXT NOT NULL PRIMARY KEY
                )
            '''
        )
        connection.commit()

    def fetchCuteness(self, userId: str, userName: str):
        if userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT cuteness FROM cuteness WHERE userId = ?', ( userId, ))
        row = cursor.fetchone()

        cuteness = 0
        if row != None:
            cuteness = row[0]

        cursor.close()
        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        return cuteness

    def fetchIncrementedCuteness(self, userId: str, userName: str, isDoublePoints: bool = False):
        if userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif isDoublePoints == None:
            raise ValueError(f'isDoublePoints argument is malformed: \"{isDoublePoints}\"')

        connection = self.__backingDatabase.getConnection()
        cursor = connection.cursor()
        cursor.execute('SELECT cuteness FROM cuteness WHERE userId = ?', ( userId, ))
        row = cursor.fetchone()

        cuteness = 0
        if row != None:
            cuteness = row[0]

        if isDoublePoints:
            cuteness = cuteness + 2
        else:
            cuteness = cuteness + 1

        cursor.execute(
            '''
                INSERT INTO cuteness (cuteness, userId)
                VALUES (?, ?)
                ON CONFLICT(userId) DO UPDATE SET cuteness = excluded.cuteness
            ''',
            ( cuteness, userId )
        )

        connection.commit()
        cursor.close()
        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        return cuteness

    def fetchLeaderboard(self, size: int = 10):
        if size == None:
            raise ValueError(f'size argument is malformed: \"{size}\"')
        elif size < 1 or size > 10:
            raise ValueError(f'size argument is out of bounds: \"{size}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE cuteness IS NOT NULL AND cuteness >= 1
                ORDER BY cuteness DESC
                LIMIT ?
            ''',
            ( size, )
        )

        rows = cursor.fetchmany(size = size)
        leaderboard = list()

        if len(rows) == 0:
            return leaderboard

        rank = 1

        for row in rows:
            userName = self.__userIdsRepository.fetchUserName(row[1])
            leaderboard.append(f'#{rank} {userName} ({row[0]})')
            rank = rank + 1

        cursor.close()
        return leaderboard
