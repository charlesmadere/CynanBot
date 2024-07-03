from __future__ import annotations

import traceback
from collections import defaultdict
from datetime import datetime

from lru import LRU

from .twitchFollowingStatus import TwitchFollowingStatus
from .twitchFollowingStatusRepositoryInterface import \
    TwitchFollowingStatusRepositoryInterface
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..api.twitchFollower import TwitchFollower
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...storage.backingDatabase import BackingDatabase
from ...storage.databaseConnection import DatabaseConnection
from ...storage.databaseType import DatabaseType
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchFollowingStatusRepository(TwitchFollowingStatusRepositoryInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheSize: int = 32
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__isDatabaseReady: bool = False
        self.__caches: dict[str, LRU[str, TwitchFollowingStatus | None]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('TwitchFollowerRepository', 'Caches cleared')

    async def fetchFollowingStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
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
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        if followingStatus is not None:
            self.__caches[twitchChannelId][userId] = followingStatus
            return followingStatus

        followingStatus = await self.__fetchFromTwitchApi(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        if followingStatus is None:
            self.__timber.log('TwitchFollowingStatusRepository', f'Failed to fetch Twitch following status ({followingStatus=}) ({twitchChannelId=}) ({userId=})')
            return None

        await self.persistFollowingStatus(
            followedAt = followingStatus.followedAt,
            twitchChannelId = followingStatus.twitchChannelId,
            userId = followingStatus.userId
        )

        self.__caches[twitchChannelId][userId] = followingStatus
        return followingStatus

    async def __fetchFromDatabase(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchFollowingStatus | None:
        connection = await self.__getDatabaseConnection()
        record = await connection.execute(
            '''
                SELECT twitchfollowingstatus.datetime, userids.username FROM twitchfollowingstatus
                INNER JOIN userids ON twitchfollowingstatus.twitchchannelid = userids.userid
                WHERE twitchfollowingstatus.twitchchannelid = $1 AND twitchfollowingstatus.userid = $2
                LIMIT 1
            ''',
            twitchChannelId, userId
        )

        await connection.close()

        if record is None or len(record) == 0:
            return None

        userName = await self.__userIdsRepository.requireUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken
        )

        return TwitchFollowingStatus(
            followedAt = datetime.fromisoformat(record[0]),
            twitchChannel = record[1],
            twitchChannelId = twitchChannelId,
            userId = userId,
            userName = userName
        )

    async def __fetchFromTwitchApi(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchFollowingStatus | None:
        twitchChannel = await self.__userIdsRepository.requireUserName(
            userId = twitchChannelId,
            twitchAccessToken = twitchAccessToken
        )

        userName = await self.__userIdsRepository.requireUserName(
            userId = userId,
            twitchAccessToken = twitchAccessToken
        )

        twitchFollower: TwitchFollower | None = None
        exception: GenericNetworkException | None =  None

        try:
            twitchFollower = await self.__twitchApiService.fetchFollower(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
                userId = userId
            )
        except GenericNetworkException as e:
            exception = e

        if twitchFollower is None or exception is not None:
            self.__timber.log('TwitchFollowerRepository', f'Failed to fetch Twitch follower from Twitch API ({twitchFollower=}) ({twitchAccessToken=}) ({twitchChannel=}) ({twitchChannelId=}) ({userId=}): {exception}', exception, traceback.format_exc())
            return None

        return TwitchFollowingStatus(
            followedAt = twitchFollower.followedAt,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
            userName = userName
        )

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        match connection.getDatabaseType():
            case DatabaseType.POSTGRESQL:
                await connection.createTableIfNotExists(
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
                await connection.createTableIfNotExists(
                    '''
                        CREATE TABLE IF NOT EXISTS twitchfollowingstatus (
                            datetime TEXT NOT NULL,
                            twitchchannelid TEXT NOT NULL,
                            userid TEXT NOT NULL,
                            PRIMARY KEY (twitchchannelid, userid)
                        )
                    '''
                )

            case _:
                raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()

    async def persistFollowingStatus(
        self,
        followedAt: datetime,
        twitchChannelId: str,
        userId: str
    ):
        if not isinstance(followedAt, datetime):
            raise TypeError(f'followedAt argument is malformed: \"{followedAt}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO twitchfollowingstatus (datetime, twitchchannelid, userid)
                VALUES ($1, $2, $3)
                ON CONFLICT (twitchchannelid, userid) DO UPDATE SET datetime = EXCLUDED.datetime
            ''',
            followedAt.isoformat(), twitchChannelId, userId
        )

        await connection.close()
