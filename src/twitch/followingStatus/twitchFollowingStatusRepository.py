import traceback
from collections import defaultdict
from datetime import datetime
from typing import Final

from lru import LRU

from .twitchFollowingStatus import TwitchFollowingStatus
from .twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ...misc import utils as utils
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface


class TwitchFollowingStatusRepository(TwitchFollowingStatusRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        cacheSize: int = 64,
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: Final[BackingDatabase] = backingDatabase
        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService

        self.__isDatabaseReady: bool = False
        self.__caches: Final[dict[str, LRU[str, TwitchFollowingStatus | None]]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('TwitchFollowingStatusRepository', 'Caches cleared')

    async def fetchFollowingStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str,
    ) -> TwitchFollowingStatus | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        followingStatus = self.__caches[twitchChannelId].get(userId, None)

        if followingStatus is not None:
            return followingStatus

        followingStatus = await self.__fetchFromDatabase(
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        if followingStatus is not None:
            self.__caches[twitchChannelId][userId] = followingStatus
            return followingStatus

        followingStatus = await self.__fetchFromTwitchApi(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        if followingStatus is None:
            self.__timber.log('TwitchFollowingStatusRepository', f'Failed to fetch Twitch following status ({followingStatus=}) ({twitchChannelId=}) ({userId=})')
            return None

        await self.persistFollowingStatus(
            followedAt = followingStatus.followedAt,
            twitchChannelId = followingStatus.twitchChannelId,
            userId = followingStatus.userId,
        )

        self.__caches[twitchChannelId][userId] = followingStatus
        return followingStatus

    async def __fetchFromDatabase(
        self,
        twitchChannelId: str,
        userId: str,
    ) -> TwitchFollowingStatus | None:
        connection = await self.__getDatabaseConnection()
        record = await connection.execute(
            '''
                SELECT datetime FROM twitchfollowingstatus
                WHERE twitchchannelid = $1 AND userid = $2
                LIMIT 1
            ''',
            twitchChannelId, userId,
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        return TwitchFollowingStatus(
            followedAt = datetime.fromisoformat(record[0]),
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

    async def __fetchFromTwitchApi(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str,
    ) -> TwitchFollowingStatus | None:
        try:
            response = await self.__twitchApiService.fetchFollower(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
                userId = userId,
            )
        except Exception as e:
            self.__timber.log('TwitchFollowingStatusRepository', f'Failed to fetch Twitch follower from Twitch API ({twitchChannelId=}) ({userId=})', e, traceback.format_exc())
            return None

        for follower in response.data:
            if follower.userId == userId:
                return TwitchFollowingStatus(
                    followedAt = follower.followedAt,
                    twitchChannelId = twitchChannelId,
                    userId = userId,
                )

        return None

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.databaseType:
            case DatabaseType.POSTGRESQL:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchfollowingstatus (
                            datetime text NOT NULL,
                            twitchchannelid text NOT NULL,
                            userid text NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case DatabaseType.SQLITE:
                await connection.execute(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchfollowingstatus (
                            datetime TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        ) STRICT
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.databaseType}\"')

        await connection.close()

    async def isFollowing(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str,
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        followingStatus = await self.fetchFollowingStatus(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        return followingStatus is not None

    async def persistFollowingStatus(
        self,
        followedAt: datetime | None,
        twitchChannelId: str,
        userId: str,
    ):
        if followedAt is not None and not isinstance(followedAt, datetime):
            raise TypeError(f'followedAt argument is malformed: \"{followedAt}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()

        if followedAt is None:
            await connection.execute(
                '''
                    DELETE FROM twitchfollowingstatus
                    WHERE twitchchannelid = $1 AND userid = $2
                ''',
                twitchChannelId, userId,
            )
        else:
            await connection.execute(
                '''
                    INSERT INTO twitchfollowingstatus (datetime, twitchchannelid, userid)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (twitchchannelid, userid) DO UPDATE SET datetime = EXCLUDED.datetime
                ''',
                followedAt.isoformat(), twitchChannelId, userId,
            )

        await connection.close()
