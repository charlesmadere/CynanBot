from datetime import timedelta
from typing import Dict, List, Set

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.misc.timedDict import TimedDict
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchStreamType import TwitchStreamType
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface


class IsLiveOnTwitchRepository(IsLiveOnTwitchRepositoryInterface):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(minutes = 10)
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchApiService, TwitchApiServiceInterface), f"malformed {twitchApiService=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(cacheTimeDelta, timedelta), f"malformed {cacheTimeDelta=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository

        self.__cache: TimedDict = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('IsLiveOnTwitchRepository', 'Caches cleared')

    async def __fetchLiveUserDetails(
        self,
        twitchHandles: List[str],
        twitchHandlesToLiveStatus: Dict[str, bool]
    ):
        twitchHandlesToFetch: Set[str] = set()

        for twitchHandle in twitchHandles:
            if twitchHandle.lower() in twitchHandlesToLiveStatus:
                continue

            twitchHandlesToFetch.add(twitchHandle.lower())

        if not utils.hasItems(twitchHandlesToFetch):
            return

        userName = await self.__administratorProvider.getAdministratorUserName()

        await self.__twitchTokensRepository.validateAndRefreshAccessToken(userName)
        twitchAccessToken = await self.__twitchTokensRepository.requireAccessToken(userName)

        liveUserDetails = await self.__twitchApiService.fetchLiveUserDetails(
            twitchAccessToken = twitchAccessToken,
            userNames = list(twitchHandlesToFetch)
        )

        for liveUserDetail in liveUserDetails:
            isLive = liveUserDetail.getStreamType() is TwitchStreamType.LIVE
            twitchHandlesToLiveStatus[liveUserDetail.getUserName().lower()] = isLive
            self.__cache[liveUserDetail.getUserName().lower()] = isLive

        for twitchHandle in twitchHandles:
            if twitchHandle.lower() not in twitchHandlesToLiveStatus:
                twitchHandlesToLiveStatus[twitchHandle.lower()] = False
                self.__cache[twitchHandle.lower()] = False

    async def isLive(self, twitchHandles: List[str]) -> Dict[str, bool]:
        twitchHandlesToLiveStatus: Dict[str, bool] = dict()

        if not utils.hasItems(twitchHandles):
            return twitchHandlesToLiveStatus

        await self.__populateFromCache(
            twitchHandles = twitchHandles,
            twitchHandlesToLiveStatus = twitchHandlesToLiveStatus
        )

        await self.__fetchLiveUserDetails(
            twitchHandles = twitchHandles,
            twitchHandlesToLiveStatus = twitchHandlesToLiveStatus
        )

        return twitchHandlesToLiveStatus

    async def __populateFromCache(
        self,
        twitchHandles: List[str],
        twitchHandlesToLiveStatus: Dict[str, bool]
    ):
        for twitchHandle in twitchHandles:
            isLive = self.__cache[twitchHandle.lower()]

            if utils.isValidBool(isLive):
                twitchHandlesToLiveStatus[twitchHandle.lower()] = isLive
