import traceback
from datetime import timedelta
from typing import Collection, Final

from frozendict import frozendict

from .isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..api.models.twitchFetchStreamsWithIdsRequest import TwitchFetchStreamsWithIdsRequest
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
        cacheTimeDelta: timedelta = timedelta(minutes = 10),
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

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository

        self.__cache: Final[TimedDict[bool]] = TimedDict(cacheTimeDelta)

    async def areLive(
        self,
        twitchChannelIds: Collection[str],
    ) -> frozendict[str, bool]:
        if not isinstance(twitchChannelIds, Collection):
            raise TypeError(f'twitchChannelIds argument is malformed: \"{twitchChannelIds}\"')

        frozenTwitchChannelIds: frozenset[str] = frozenset(twitchChannelIds)
        twitchChannelIdToLiveStatus: dict[str, bool] = dict()

        if len(frozenTwitchChannelIds) == 0:
            return frozendict(twitchChannelIdToLiveStatus)

        await self.__populateFromCache(
            twitchChannelIds = frozenTwitchChannelIds,
            twitchChannelIdToLiveStatus = twitchChannelIdToLiveStatus,
        )

        await self.__fetchLiveUserDetails(
            twitchChannelIds = frozenTwitchChannelIds,
            twitchChannelIdToLiveStatus = twitchChannelIdToLiveStatus,
        )

        return frozendict(twitchChannelIdToLiveStatus)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('IsLiveOnTwitchRepository', 'Caches cleared')

    async def __fetchLiveUserDetails(
        self,
        twitchChannelIds: frozenset[str],
        twitchChannelIdToLiveStatus: dict[str, bool],
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

        try:
            streamsResponse = await self.__twitchApiService.fetchStreams(
                twitchAccessToken = twitchAccessToken,
                fetchStreamsRequest = TwitchFetchStreamsWithIdsRequest(
                    userIds = frozenset(twitchChannelIdsToFetch),
                ),
            )
        except Exception as e:
            self.__timber.log('IsLiveOnTwitchRepository', f'Failed to fetch live user details ({twitchChannelIdsToFetch=})', e, traceback.format_exc())
            return

        for stream in streamsResponse.data:
            isLive = stream.streamType is TwitchStreamType.LIVE
            twitchChannelIdToLiveStatus[stream.userId] = isLive
            self.__cache[stream.userId] = isLive

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
        twitchChannelIds: frozenset[str],
        twitchChannelIdToLiveStatus: dict[str, bool]
    ):
        for twitchChannelId in twitchChannelIds:
            isLive = self.__cache[twitchChannelId]

            if utils.isValidBool(isLive):
                twitchChannelIdToLiveStatus[twitchChannelId] = isLive
