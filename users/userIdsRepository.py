import aiohttp
import CynanBotCommon.utils as utils
from aiosqlite import Connection
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.timber.timber import Timber


class UserIdsRepository():

    def __init__(
        self,
        clientSession: aiohttp.ClientSession,
        backingDatabase: BackingDatabase,
        timber: Timber
    ):
        if clientSession is None:
            raise ValueError(f'clientSession argument is malformed: \"{clientSession}\"')
        elif backingDatabase is None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__clientSession: aiohttp.ClientSession = clientSession
        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: Timber = timber

        self.__isDatabaseReady: bool = False

    async def fetchUserId(
        self,
        userName: str,
        twitchAccessToken: str = None,
        twitchClientId: str = None
    ) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                SELECT userId FROM userIds
                WHERE userName = ?
            ''',
            ( userName, )
        )

        row = await cursor.fetchone()

        userId: str = None
        if row is not None:
            userId = row[0]

        await cursor.close()
        await connection.close()

        if userId is not None:
            if utils.isValidStr(userId):
                return userId
            else:
                raise RuntimeError(f'Persisted userId for userName \"{userName}\" is malformed: \"{userId}\"')

        if not utils.isValidStr(twitchAccessToken) or not utils.isValidStr(twitchClientId):
            raise ValueError(f'Can\'t lookup Twitch user ID for \"{userName}\", as twitchAccessToken (\"{twitchAccessToken}\") and/or twitchClientId (\"{twitchClientId}\") is malformed')

        self.__timber.log('UserIdsRepository', f'Performing network call to fetch Twitch user ID for \"{userName}\"...')

        response = await self.__clientSession.get(
            url = f'https://api.twitch.tv/helix/users?login={userName}',
            headers = {
                'Authorization': f'Bearer {twitchAccessToken}',
                'Client-Id': twitchClientId
            }
        )

        jsonResponse = await response.json()
        response.close()

        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            raise RuntimeError(f'Received an error when fetching user ID for {userName}: {jsonResponse}')

        userId: str = jsonResponse['data'][0]['id']

        if not utils.isValidStr(userId):
            raise ValueError(f'Unable to fetch user ID for \"{userName}\": {jsonResponse}')

        await self.setUser(userId = userId, userName = userName)
        return userId

    async def fetchUserIdAsInt(
        self,
        userName: str,
        twitchAccessToken: str = None,
        twitchClientId: str = None
    ) -> int:
        userId = await self.fetchUserId(
            userName = userName,
            twitchAccessToken = twitchAccessToken,
            twitchClientId = twitchClientId
        )

        return int(userId)

    async def fetchUserName(self, userId: str) -> str:
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                SELECT userName FROM userIds
                WHERE userId = ?
            ''',
            ( userId, )
        )

        row = await cursor.fetchone()

        if row is None:
            raise RuntimeError(f'No userName for userId \"{userId}\" found')

        userName: str = row[0]
        if not utils.isValidStr(userName):
            raise RuntimeError(f'userName for userId \"{userId}\" is malformed: \"{userName}\"')

        await cursor.close()
        await connection.close()
        return userName

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
                CREATE TABLE IF NOT EXISTS userIds (
                    userId TEXT NOT NULL PRIMARY KEY COLLATE NOCASE,
                    userName TEXT NOT NULL COLLATE NOCASE
                )
            '''
        )

        await connection.commit()
        await cursor.close()
        await connection.close()

    async def setUser(self, userId: str, userName: str):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userId == '0':
            raise ValueError(f'userId argument is an illegal value: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        connection = await self.__getDatabaseConnection()
        cursor = await connection.execute(
            '''
                INSERT INTO userIds (userId, userName)
                VALUES (?, ?)
                ON CONFLICT (userId) DO UPDATE SET userName = excluded.userName
            ''',
            ( userId, userName )
        )

        await connection.commit()
        await cursor.close()
        await connection.close()
