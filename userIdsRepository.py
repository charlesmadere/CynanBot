from backingDatabase import BackingDatabase
import json
import requests

class UserIdsRepository():

    def __init__(self, backingDatabase: BackingDatabase):
        if backingDatabase == None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase = backingDatabase

        connection = backingDatabase.getConnection()
        connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS userIds (
                    userId TEXT NOT NULL PRIMARY KEY,
                    userName TEXT NOT NULL
                )
            '''
        )
        connection.commit()

    def fetchUserName(self, userId: str):
        if userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT userName FROM userIds WHERE userId = ?', ( userId, ))
        row = cursor.fetchone()

        if row == None:
            raise RuntimeError(f'No userName for userId \"{userId}\" found')

        userName = row[0]
        if userName == None or len(userName) == 0 or userName.isspace():
            raise RuntimeError(f'userName for userId \"{userId}\" is malformed: \"{userName}\"')

        cursor.close()
        return userName

    def fetchUserId(self, userName: str, clientId: str, accessToken: str):
        if userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif clientId == None or len(clientId) == 0 or clientId.isspace():
            raise ValueError(f'clientId argument is malformed: \"{clientId}\"')
        elif accessToken == None or len(accessToken) == 0 or accessToken.isspace():
            raise ValueError(f'accessToken argument is malformed: \"{accessToken}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT userId FROM userIds WHERE userName = ?', ( userName, ))
        row = cursor.fetchone()

        userId = None
        if row != None:
            userId = row[0]

        cursor.close()

        if userId != None:
            if len(userId) == 0 or userId.isspace():
                raise RuntimeError(f'Persisted userId for userName \"{userName}\" is malformed: \"{userId}\"')
            else:
                return userId

        headers = {
            'Client-ID': clientId,
            'Authorization': f'Bearer {accessToken}'
        }

        rawResponse = requests.get(
            url = f'https://api.twitch.tv/helix/users?login={userName}',
            headers = headers
        )

        jsonResponse = json.loads(rawResponse.content)

        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            raise RuntimeError(f'Received an error when fetching user ID for {userName}: {jsonResponse}')

        userId = jsonResponse['data'][0]['id']

        if userId == None or len(userId) == 0 or userId.isspace():
            raise ValueError(f'Unable to fetch user ID for {userName}: {jsonResponse}')

        self.setUser(userId = userId, userName = userName)

        return userId

    def setUser(self, userId: str, userName: str):
        if userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        connection = self.__backingDatabase.getConnection()
        cursor = connection.cursor()
        cursor.execute(
            '''
                INSERT INTO userIds (userId, userName)
                VALUES (?, ?)
                ON CONFLICT(userId) DO UPDATE SET userName = excluded.userName
            ''',
            ( userId, userName )
        )
        connection.commit()
        cursor.close()
