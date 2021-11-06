import requests
from requests import ConnectionError, HTTPError, Timeout
from requests.exceptions import ReadTimeout, TooManyRedirects
from urllib3.exceptions import MaxRetryError, NewConnectionError

import CynanBotCommon.utils as utils
from CynanBotCommon.backingDatabase import BackingDatabase


class UserIdsRepository():

    def __init__(self, backingDatabase: BackingDatabase):
        if backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase

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
        twitchAccessToken: str = None,
        twitchClientId: str = None
    ) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT userId FROM userIds WHERE userName = ?', ( userName, ))
        row = cursor.fetchone()

        userId: str = None
        if row is not None:
            userId = row[0]

        cursor.close()

        if userId is not None:
            if utils.isValidStr(userId):
                return userId
            else:
                raise RuntimeError(f'Persisted userId for userName \"{userName}\" is malformed: \"{userId}\"')

        if not utils.isValidStr(twitchAccessToken) or not utils.isValidStr(twitchClientId):
            raise ValueError(f'Can\'t lookup Twitch user ID for \"{userName}\", as twitchAccessToken (\"{twitchAccessToken}\") and/or twitchClientId (\"{twitchClientId}\") is malformed')

        print(f'Performing network call to fetch Twitch user ID for \"{userName}\"... ({utils.getNowTimeText(includeSeconds = True)})')

        rawResponse = None
        try:
            rawResponse = requests.get(
                url = f'https://api.twitch.tv/helix/users?login={userName}',
                headers = {
                    'Authorization': f'Bearer {twitchAccessToken}',
                    'Client-Id': twitchClientId
                },
                timeout = utils.getDefaultTimeout()
            )
        except (ConnectionError, HTTPError, MaxRetryError, NewConnectionError, ReadTimeout, Timeout, TooManyRedirects) as e:
            print(f'Exception occurred when attempting to fetch user ID for \"{userName}\": {e}')
            raise RuntimeError(f'Exception occurred when attempting to fetch user ID for \"{userName}\": {e}')

        jsonResponse = rawResponse.json()

        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            raise RuntimeError(f'Received an error when fetching user ID for {userName}: {jsonResponse}')

        userId = jsonResponse['data'][0]['id']

        if not utils.isValidStr(userId):
            raise ValueError(f'Unable to fetch user ID for \"{userName}\": {jsonResponse}')

        self.setUser(userId = userId, userName = userName)
        return userId

    def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str = None,
        twitchClientId: str = None
    ) -> int:
        userId = self.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken,
            twitchClientId = twitchClientId
        )

        return int(userId)

    def fetchUserName(self, userId: str) -> str:
        if not utils.isValidStr(userId) or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute('SELECT userName FROM userIds WHERE userId = ?', ( userId, ))
        row = cursor.fetchone()

        if row is None:
            raise RuntimeError(f'No userName for userId \"{userId}\" found')

        userName: str = row[0]
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
                ON CONFLICT (userId) DO UPDATE SET userName = excluded.userName
            ''',
            ( userId, userName )
        )
        connection.commit()
        cursor.close()
