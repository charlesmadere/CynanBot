import traceback
from datetime import timedelta

from .twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..api.twitchEmotesResponse import TwitchEmotesResponse
from ..api.twitchEmoteType import TwitchEmoteType
from ..api.twitchThemeMode import TwitchThemeMode
from ...misc import utils as utils
from ...misc.timedDict import TimedDict
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class TwitchEmotesHelper(TwitchEmotesHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService

        self.__cache: TimedDict[set[str]] = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TwitchEmotesHelper', 'Caches cleared')

    async def fetchViableEmoteNamesFor(
        self,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> set[str]:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        viableEmoteNames = self.__cache[twitchChannelId]
        if viableEmoteNames is not None:
            return viableEmoteNames

        response: TwitchEmotesResponse | None = None

        try:
            response = await self.__twitchApiService.fetchEmotes(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken
            )
        except GenericNetworkException as e:
            self.__timber.log('TwitchEmotesHelper', f'Encountered network error when fetching emotes ({twitchAccessToken=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())

        viableEmoteNames = await self.__processTwitchResponseIntoViableSubscriptionEmotes(response)
        self.__cache[twitchChannelId] = viableEmoteNames
        return viableEmoteNames

    async def __processTwitchResponseIntoViableSubscriptionEmotes(
        self,
        response: TwitchEmotesResponse | None
    ) -> set[str]:
        if response is not None and not isinstance(response, TwitchEmotesResponse):
            raise TypeError(f'response argument is malformed: \"{response}\"')

        viableEmoteNames: set[str] = set()

        if response is None or len(response.emoteData) == 0:
            return viableEmoteNames

        allThemeModes = set(TwitchThemeMode)

        for emote in response.emoteData:
            if emote.emoteType is not TwitchEmoteType.SUBSCRIPTIONS:
                break

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

        return viableEmoteNames
