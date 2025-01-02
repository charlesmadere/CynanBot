from datetime import timedelta

from frozendict import frozendict

from .isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..api.models.twitchStreamType import TwitchStreamType
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...misc.timedDict import TimedDict
from ...timber.timberInterface import TimberInterface


class IsLiveOnTwitchRepository(IsLiveOnTwitchRepositoryInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(minutes = 10)
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository

        self.__cache: TimedDict[bool] = TimedDict(cacheTimeDelta)

    async def areLive(self, twitchChannelIds: set[str]) -> frozendict[str, bool]:
        if not isinstance(twitchChannelIds, set):
            raise TypeError(f'twitchChannelIds argument is malformed: \"{twitchChannelIds}\"')

        twitchChannelIdToLiveStatus: dict[str, bool] = dict()

        if len(twitchChannelIds) == 0:
            return frozendict(twitchChannelIdToLiveStatus)

        await self.__populateFromCache(
            twitchChannelIds = twitchChannelIds,
            twitchChannelIdToLiveStatus = twitchChannelIdToLiveStatus
        )

        await self.__fetchLiveUserDetails(
            twitchChannelIds = twitchChannelIds,
            twitchChannelIdToLiveStatus = twitchChannelIdToLiveStatus
        )

        return frozendict(twitchChannelIdToLiveStatus)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('IsLiveOnTwitchRepository', 'Caches cleared')

    async def __fetchLiveUserDetails(
        self,
        twitchChannelIds: set[str],
        twitchChannelIdToLiveStatus: dict[str, bool]
    ):
        twitchChannelIdsToFetch: set[str] = set()

        for twitchChannelId in twitchChannelIds:
            if twitchChannelId in twitchChannelIdToLiveStatus:
                continue

            twitchChannelIdsToFetch.add(twitchChannelId)

        if len(twitchChannelIdsToFetch) == 0:
            return

        userId = await self.__administratorProvider.getAdministratorUserId()
        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(userId)

        liveUserDetails = await self.__twitchApiService.fetchLiveUserDetails(
            twitchAccessToken = twitchAccessToken,
            twitchChannelIds = list(twitchChannelIdsToFetch)
        )

        for liveUserDetail in liveUserDetails:
            isLive = liveUserDetail.streamType is TwitchStreamType.LIVE
            twitchChannelIdToLiveStatus[liveUserDetail.userId] = isLive
            self.__cache[liveUserDetail.userId] = isLive

        for twitchChannelId in twitchChannelIds:
            if twitchChannelId not in twitchChannelIdToLiveStatus:
                twitchChannelIdToLiveStatus[twitchChannelId] = False
                self.__cache[twitchChannelId] = False

    async def isLive(self, twitchChannelId: str) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchChannelIds: set[str] = set()
        twitchChannelIds.add(twitchChannelId)

        twitchChannelIdsToLiveStatus = await self.areLive(twitchChannelIds)
        return twitchChannelIdsToLiveStatus.get(twitchChannelId, False) is True

    async def __populateFromCache(
        self,
        twitchChannelIds: set[str],
        twitchChannelIdToLiveStatus: dict[str, bool]
    ):
        for twitchChannelId in twitchChannelIds:
            isLive = self.__cache[twitchChannelId]

            if utils.isValidBool(isLive):
                twitchChannelIdToLiveStatus[twitchChannelId] = isLive
