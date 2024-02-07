from datetime import timedelta
import traceback
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.timedDict import TimedDict
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchFollower import TwitchFollower
from CynanBot.twitch.twitchFollowerRepositoryInterface import TwitchFollowerRepositoryInterface
from CynanBot.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from CynanBot.twitch.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from CynanBot.network.exceptions import GenericNetworkException


class TwitchFollowerRepository(TwitchFollowerRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 8)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__cache: TimedDict = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchFollowerRepository', f'Caches cleared')

    async def fetchFollowingInfo(
        self,
        twitchAccessToken: Optional[str],
        twitchChannelId: str,
        userId: str
    ) -> Optional[TwitchFollower]:
        if twitchAccessToken is not None and not isinstance(twitchAccessToken, str):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        follower: Optional[TwitchFollower] = self.__cache[f'{twitchChannelId}:{userId}']

        if follower is not None:
            return follower

        twitchChannel = await self.__userIdsRepository.requireUserName(userId = twitchChannelId)

        if not utils.isValidStr(twitchAccessToken):
            twitchAccessToken = await self.__twitchTokensUtils.requireAccessTokenOrFallback(twitchChannel)

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

        self.__cache[f'{twitchChannelId}:{userId}'] = follower
        return follower
