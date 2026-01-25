import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final

from .twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..api.models.twitchEmoteType import TwitchEmoteType
from ..api.models.twitchEmotesResponse import TwitchEmotesResponse
from ..api.models.twitchThemeMode import TwitchThemeMode
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import TwitchStatusCodeException, TwitchJsonException
from ..handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..subscribers.twitchSubscriptionStatus import TwitchSubscriptionStatus
from ..subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchEmotesHelper(TwitchEmotesHelperInterface):

    @dataclass(frozen = True, slots = True)
    class Entry:
        fetchDateTime: datetime
        availableEmotes: frozenset[str]
        twitchChannelId: str

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 3),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchSubscriptionsRepository: Final[TwitchSubscriptionsRepositoryInterface] = twitchSubscriptionsRepository
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__cacheTimeDelta: Final[timedelta] = cacheTimeDelta

        self.__cache: Final[dict[str, TwitchEmotesHelper.Entry | None]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchEmotesHelper', 'Caches cleared')

    async def __fetchFromTwitchApi(
        self,
        twitchChannelId: str,
    ) -> Entry | None:
        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchId = await self.__userIdsRepository.requireUserId(twitchHandle)
        twitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(twitchId)

        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('TwitchEmotesHelper', f'No Twitch access token is available to use for fetching viable subscription emotes ({twitchChannelId=})')
            return None

        emotesResponse: TwitchEmotesResponse | None = None
        subscriptionStatus: TwitchSubscriptionStatus | None = None

        try:
            emotesResponse = await self.__twitchApiService.fetchChannelEmotes(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
            )

            subscriptionStatus = await self.__twitchSubscriptionsRepository.fetchSelfSubscription(
                twitchAccessToken = twitchAccessToken,
                twitchChannelId = twitchChannelId,
            )
        except (GenericNetworkException, TwitchJsonException, TwitchStatusCodeException) as e:
            self.__timber.log('TwitchEmotesHelper', f'Encountered network error when fetching either subscription status or emotes ({twitchChannelId=}) ({emotesResponse=}) ({subscriptionStatus=})', e, traceback.format_exc())

        viableEmoteNames = await self.__processTwitchResponseIntoViableSubscriptionEmotes(
            emotesResponse = emotesResponse,
            subscriptionStatus = subscriptionStatus,
        )

        self.__timber.log('TwitchEmotesHelper', f'Fetched {len(viableEmoteNames)} viable emote name(s) ({twitchChannelId=}) ({subscriptionStatus=}) ({viableEmoteNames=})')

        return TwitchEmotesHelper.Entry(
            fetchDateTime = datetime.now(self.__timeZoneRepository.getDefault()),
            availableEmotes = viableEmoteNames,
            twitchChannelId = twitchChannelId,
        )

    async def fetchViableSubscriptionEmoteNames(
        self,
        twitchChannelId: str,
    ) -> frozenset[str]:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        cachedEntry = await self.__getCachedEntry(twitchChannelId = twitchChannelId)

        if cachedEntry is not None:
            return cachedEntry.availableEmotes

        entry = await self.__fetchFromTwitchApi(twitchChannelId = twitchChannelId)

        if entry is None:
            entry = TwitchEmotesHelper.Entry(
                fetchDateTime = datetime.now(self.__timeZoneRepository.getDefault()),
                availableEmotes = frozenset(),
                twitchChannelId = twitchChannelId,
            )

        self.__cache[twitchChannelId] = entry
        return entry.availableEmotes

    async def __getCachedEntry(
        self,
        twitchChannelId: str,
    ) -> Entry | None:
        cachedEntry = self.__cache.get(twitchChannelId, None)

        if cachedEntry is None:
            return None

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if cachedEntry.fetchDateTime + self.__cacheTimeDelta >= now:
            return cachedEntry
        else:
            return None

    async def __processTwitchResponseIntoViableSubscriptionEmotes(
        self,
        emotesResponse: TwitchEmotesResponse | None,
        subscriptionStatus: TwitchSubscriptionStatus | None,
    ) -> frozenset[str]:
        if emotesResponse is not None and not isinstance(emotesResponse, TwitchEmotesResponse):
            raise TypeError(f'emotesResponse argument is malformed: \"{emotesResponse}\"')
        elif subscriptionStatus is not None and not isinstance(subscriptionStatus, TwitchSubscriptionStatus):
            raise TypeError(f'userSubscription argument is malformed: \"{subscriptionStatus}\"')

        if subscriptionStatus is None or emotesResponse is None or len(emotesResponse.emoteData) == 0:
            return frozenset()

        viableEmoteNames: set[str] = set()
        allThemeModes = frozenset(TwitchThemeMode)

        for emote in emotesResponse.emoteData:
            if emote.emoteType is not TwitchEmoteType.SUBSCRIPTIONS:
                continue

            foundThemeModes: set[TwitchThemeMode] = set()
            add = True

            for themeMode in emote.themeModes:
                foundThemeModes.add(themeMode)

            for themeMode in allThemeModes:
                if themeMode not in foundThemeModes:
                    add = False
                    break

            if add:
                viableEmoteNames.add(emote.name)

        return frozenset(viableEmoteNames)
