import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Collection, Final

from frozendict import frozendict

from .isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..api.models.twitchFetchStreamsWithIdsRequest import TwitchFetchStreamsWithIdsRequest
from ..api.models.twitchStream import TwitchStream
from ..api.models.twitchStreamType import TwitchStreamType
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...timber.timberInterface import TimberInterface


class IsLiveOnTwitchRepository(IsLiveOnTwitchRepositoryInterface):

    @dataclass(frozen = True, slots = True)
    class LiveStreamStatusEntry:
        expiresAt: datetime
        twitchChannelId: str
        twitchStream: TwitchStream | None

        @property
        def isLive(self) -> bool:
            return self.twitchStream is not None and self.twitchStream.streamType is TwitchStreamType.LIVE

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cacheTimeToLive: timedelta = timedelta(minutes = 5),
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__cacheTimeToLive: Final[timedelta] = cacheTimeToLive

        self.__cache: Final[dict[str, IsLiveOnTwitchRepository.LiveStreamStatusEntry | None]] = dict()

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

        administratorUserId = await self.__administratorProvider.getAdministratorUserId()

        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = administratorUserId,
        )

        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('IsLiveOnTwitchRepository', f'No Twitch access token available to check for live user details ({twitchChannelIdsToFetch=}) ({administratorUserId=})')
            return

        now = datetime.now(self.__timeZoneRepository.getDefault())

        try:
            streamsResponse = await self.__twitchApiService.fetchStreams(
                twitchAccessToken = twitchAccessToken,
                fetchStreamsRequest = TwitchFetchStreamsWithIdsRequest(
                    userIds = frozenset(twitchChannelIdsToFetch),
                ),
            )
        except Exception as e:
            self.__timber.log('IsLiveOnTwitchRepository', f'Failed to fetch live user details ({twitchChannelIdsToFetch=}) ({administratorUserId=})', e, traceback.format_exc())
            return

        for stream in streamsResponse.data:
            liveStreamStatusEntry = IsLiveOnTwitchRepository.LiveStreamStatusEntry(
                expiresAt = now + self.__cacheTimeToLive,
                twitchChannelId = stream.userId,
                twitchStream = stream,
            )

            twitchChannelIdToLiveStatus[stream.userId] = liveStreamStatusEntry.isLive
            self.__cache[stream.userId] = liveStreamStatusEntry

        for twitchChannelId in twitchChannelIds:
            if twitchChannelId not in twitchChannelIdToLiveStatus:
                twitchChannelIdToLiveStatus[twitchChannelId] = False
                self.__cache[twitchChannelId] = IsLiveOnTwitchRepository.LiveStreamStatusEntry(
                    expiresAt = now + self.__cacheTimeToLive,
                    twitchChannelId = twitchChannelId,
                    twitchStream = None,
                )

    async def isLive(self, twitchChannelId: str) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchChannelIds: frozenset[str] = frozenset({ twitchChannelId })
        twitchChannelIdsToLiveStatus = await self.areLive(twitchChannelIds)
        return twitchChannelIdsToLiveStatus.get(twitchChannelId, False) is True

    async def __populateFromCache(
        self,
        twitchChannelIds: frozenset[str],
        twitchChannelIdToLiveStatus: dict[str, bool],
    ):
        now = datetime.now(self.__timeZoneRepository.getDefault())

        for twitchChannelId in twitchChannelIds:
            cachedEntry = self.__cache.get(twitchChannelId, None)

            if cachedEntry is not None and cachedEntry.expiresAt >= now:
                twitchChannelIdToLiveStatus[twitchChannelId] = cachedEntry.isLive
