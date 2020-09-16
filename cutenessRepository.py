import sqlite3

class CutenessRepository():
    def __init__(self, cutenessDatabase: str = 'cutenessDatabase.sqlite'):
        if cutenessDatabase == None or len(cutenessDatabase) == 0 or cutenessDatabase.isspace():
            raise ValueError(f'cutenessDatabase argument is malformed: \"{cutenessDatabase}\"')

        self.__databaseConnection = sqlite3.connect(cutenessDatabase)

        self.__databaseConnection.execute(
            '''
                CREATE TABLE IF NOT EXISTS cuteness (
                    cuteness INTEGER NOT NULL DEFAULT 0,
                    userId TEXT NOT NULL PRIMARY KEY,
                    userName TEXT NOT NULL
                )
            '''
        )

        self.__databaseConnection.commit()

    def getCuteness(self, userId: str, userName: str):
        if userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        cursor = self.__databaseConnection.cursor()
        cursor.execute('SELECT cuteness FROM cuteness WHERE userId = ?', ( userId, ))
        row = cursor.fetchone()

        cuteness = 0
        if row == None:
            cursor.execute('INSERT INTO cuteness (userId, userName) VALUES (?, ?)', ( userId, userName ))
        else:
            cuteness = row[0]
            cursor.execute('UPDATE cuteness SET userName = ? WHERE userId = ?', ( userName, userId ))

        self.__databaseConnection.commit()
        return cuteness

    def getIncrementedCuteness(self, userId: str, userName: str):
        if userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        cursor = self.__databaseConnection.cursor()
        cursor.execute('SELECT cuteness FROM cuteness WHERE userId = ?', ( userId, ))
        row = cursor.fetchone()

        cuteness = 0
        if row != None:
            cuteness = row[0]

        cuteness = cuteness + 1

        if row == None:
            cursor.execute('INSERT INTO cuteness (cuteness, userId, userName) VALUES (?, ?, ?)', ( cuteness, userId, userName ))
        else:
            cursor.execute('UPDATE cuteness SET cuteness = ?, userName = ? WHERE userId = ?', ( cuteness, userName, userId ))

        self.__databaseConnection.commit()
        return cuteness

    def getLeaderboard(self, size: int = 5):
        if size == None:
            raise ValueError(f'size argument is malformed: \"{size}\"')
        elif size < 1 or size > 10:
            raise ValueError(f'size argument is out of bounds: \"{size}\"')

        cursor = self.__databaseConnection.cursor()
        cursor.execute(
            '''
                SELECT userName, cuteness FROM cuteness
                WHERE cuteness IS NOT NULL AND cuteness >= 1
                ORDER BY cuteness DESC, userName ASC
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
            leaderboard.append(f'#{rank} {row[0]} ({row[1]})')
            rank = rank + 1

        return leaderboard
