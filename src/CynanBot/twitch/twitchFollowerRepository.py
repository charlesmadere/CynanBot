import traceback
from collections import defaultdict
from datetime import timedelta

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
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__cache: dict[str, TimedDict[TwitchFollower]] = defaultdict(lambda: TimedDict(cacheTimeDelta))

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchFollowerRepository', f'Caches cleared')

    async def fetchFollowingInfo(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchFollower | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        follower = self.__cache[twitchChannelId][userId]

        if follower is not None:
            return follower

        twitchChannel = await self.__userIdsRepository.requireUserName(userId = twitchChannelId)
        exception: GenericNetworkException | None = None

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
