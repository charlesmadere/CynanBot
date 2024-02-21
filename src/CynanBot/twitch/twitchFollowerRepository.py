import traceback
from collections import defaultdict
from datetime import timedelta
from typing import Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.timedDict import TimedDict
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchFollower import TwitchFollower
from CynanBot.twitch.twitchFollowerRepositoryInterface import \
    TwitchFollowerRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TwitchFollowerRepository(TwitchFollowerRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 8)
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchApiService, TwitchApiServiceInterface), f"malformed {twitchApiService=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(cacheTimeDelta, timedelta), f"malformed {cacheTimeDelta=}"

        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__cache: Dict[str, TimedDict] = defaultdict(lambda: TimedDict(cacheTimeDelta))

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchFollowerRepository', f'Caches cleared')

    async def fetchFollowingInfo(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> Optional[TwitchFollower]:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        follower: Optional[TwitchFollower] = self.__cache[twitchChannelId][userId]

        if follower is not None:
            return follower

        twitchChannel = await self.__userIdsRepository.requireUserName(userId = twitchChannelId)
        exception: Optional[GenericNetworkException] = None

        try:
            follower = await self.__twitchApiService.fetchFollower(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
                userId = userId
            )
        except GenericNetworkException as e:
            exception = e

        if follower is None or exception is not None:
            self.__timber.log('TwitchFollowerRepository', f'Failed to fetch Twitch follower ({twitchAccessToken=}) ({twitchChannel=}) ({twitchChannelId}) ({userId=}): {exception}', exception, traceback.format_exc())
            return None

        self.__cache[twitchChannelId][userId] = follower
        return follower
