import traceback
from datetime import timedelta

from .twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..api.twitchBroadcasterSubscriptionResponse import TwitchBroadcasterSubscriptionResponse
from ..api.twitchEmoteType import TwitchEmoteType
from ..api.twitchEmotesResponse import TwitchEmotesResponse
from ..api.twitchThemeMode import TwitchThemeMode
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...misc import utils as utils
from ...misc.timedDict import TimedDict
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchEmotesHelper(TwitchEmotesHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 3)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

        self.__cache: TimedDict[frozenset[str]] = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchEmotesHelper', 'Caches cleared')

    async def fetchViableSubscriptionEmoteNames(
        self,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> frozenset[str]:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        viableEmoteNames = self.__cache[twitchChannelId]
        if viableEmoteNames is not None:
            return viableEmoteNames

        twitchId = await self.__getTwitchId(twitchAccessToken)
        broadcasterSubscription: TwitchBroadcasterSubscriptionResponse | None = None
        emotesResponse: TwitchEmotesResponse | None = None

        try:
            broadcasterSubscription = await self.__twitchApiService.fetchBroadcasterSubscription(
                broadcasterId = twitchChannelId,
                chatterUserId = twitchId,
                twitchAccessToken = twitchAccessToken
            )

            emotesResponse = await self.__twitchApiService.fetchEmotes(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchEmotesHelper', f'Encountered network error when fetching either broadcaster subscription or emotes ({twitchAccessToken=}) ({twitchChannelId=}) ({twitchId=}) ({broadcasterSubscription=}) ({emotesResponse=}): {e}', e, traceback.format_exc())

        viableEmoteNames = await self.__processTwitchResponseIntoViableSubscriptionEmotes(
            broadcasterSubscription = broadcasterSubscription,
            emotesResponse = emotesResponse
        )

        self.__timber.log('TwitchEmotesHelper', f'Fetched {len(viableEmoteNames)} viable emote name(s) ({viableEmoteNames=}) ({twitchAccessToken=}) ({twitchChannelId=}) ({twitchId=}) ({broadcasterSubscription=}) ({emotesResponse=})')
        self.__cache[twitchChannelId] = viableEmoteNames
        return viableEmoteNames

    async def __getTwitchId(self, twitchAccessToken: str) -> str:
        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        return await self.__userIdsRepository.requireUserId(
            userName = twitchHandle,
            twitchAccessToken = twitchAccessToken
        )

    async def __processTwitchResponseIntoViableSubscriptionEmotes(
        self,
        broadcasterSubscription: TwitchBroadcasterSubscriptionResponse | None,
        emotesResponse: TwitchEmotesResponse | None
    ) -> frozenset[str]:
        if broadcasterSubscription is not None and not isinstance(broadcasterSubscription, TwitchBroadcasterSubscriptionResponse):
            raise TypeError(f'broadcasterSubscription argument is malformed: \"{broadcasterSubscription}\"')
        elif emotesResponse is not None and not isinstance(emotesResponse, TwitchEmotesResponse):
            raise TypeError(f'emotesResponse argument is malformed: \"{emotesResponse}\"')

        viableEmoteNames: set[str] = set()

        if broadcasterSubscription is None or broadcasterSubscription.subscription is None or emotesResponse is None or len(emotesResponse.emoteData) == 0:
            return frozenset(viableEmoteNames)

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
