import requests

import CynanBotCommon.utils as utils
from CynanBotCommon.backingDatabase import BackingDatabase


class UserIdsRepository():

    def __init__(self, backingDatabase: BackingDatabase):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase = backingDatabase

        connection = backingDatabase.getConnection()
        connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS userIds (
                    userId TEXT NOT NULL PRIMARY KEY COLLATE NOCASE,
                    userName TEXT NOT NULL COLLATE NOCASE
                )
            '''
        )
        connection.commit()

    def fetchUserId(
        self,
        userName: str,
        clientId: str = None,
        accessToken: str = None
    ):
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT userId FROM userIds WHERE userName = ?', (userName, ))
        row = cursor.fetchone()

        userId = None
        if row is not None:
            userId = row[0]

        cursor.close()

        if userId is not None:
            if utils.isValidStr(userId):
                return userId
            else:
                raise RuntimeError(f'Persisted userId for userName \"{userName}\" is malformed: \"{userId}\"')

        if not utils.isValidStr(clientId):
            print(f'Can\'t lookup user ID for \"{userName}\", as clientId is malformed: \"{clientId}\"')
            raise ValueError(f'clientId argument is malformed: \"{clientId}\"')
        elif not utils.isValidStr(accessToken):
            print(f'Can\'t lookup user ID for \"{userName}\", as accessToken is malformed: \"{accessToken}\"')
            raise ValueError(f'accessToken argument is malformed: \"{accessToken}\"')

        print(f'Performing network call to fetch user ID for {userName}...')

        headers = {
            'Client-ID': clientId,
            'Authorization': f'Bearer {accessToken}'
        }

        rawResponse = requests.get(
            url = f'https://api.twitch.tv/helix/users?login={userName}',
            headers = headers,
            timeout = utils.getDefaultTimeout()
        )

        jsonResponse = rawResponse.json()

        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            raise RuntimeError(f'Received an error when fetching user ID for {userName}: {jsonResponse}')

        userId = jsonResponse['data'][0]['id']

        if not utils.isValidStr(userId):
            raise ValueError(f'Unable to fetch user ID for {userName}: {jsonResponse}')

        self.setUser(userId = userId, userName = userName)

        return userId

    def fetchUserName(self, userId: str):
        if not utils.isValidStr(userId) or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT userName FROM userIds WHERE userId = ?', (userId, ))
        row = cursor.fetchone()

        if row is None:
            raise RuntimeError(f'No userName for userId \"{userId}\" found')

        userName = row[0]
        if not utils.isValidStr(userName):
            raise RuntimeError(f'userName for userId \"{userId}\" is malformed: \"{userName}\"')

        cursor.close()
        return userName

    def setUser(self, userId: str, userName: str):
        if not utils.isValidStr(userId) or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        connection = self.__backingDatabase.getConnection()
        cursor = connection.cursor()
        cursor.execute(
            '''
                INSERT INTO userIds (userId, userName)
                VALUES (?, ?)
                ON CONFLICT(userId) DO UPDATE SET userName = excluded.userName
            ''',
            (userId, userName)
        )
        connection.commit()
        cursor.close()
