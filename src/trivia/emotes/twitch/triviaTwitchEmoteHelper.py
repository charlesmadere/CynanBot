from datetime import datetime, timedelta

from .triviaTwitchEmoteHelperInterface import TriviaTwitchEmoteHelperInterface
from .triviaTwitchEmoteType import TriviaTwitchEmoteType
from ....location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface
from ....twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ....twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ....twitch.twitchTokensUtilsInterface import TwitchTokensUtilsInterface


class TriviaTwitchEmoteHelper(TriviaTwitchEmoteHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        celebratoryEmote: str | None = 'samusHype',
        outOfTimeEmote: str | None = 'samusShrug',
        wrongAnswerEmote: str | None = 'samusBad',
        cacheTimeBuffer: timedelta = timedelta(hours = 2)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif celebratoryEmote is not None and not isinstance(celebratoryEmote, str):
            raise TypeError(f'celebratoryEmote argument is malformed: \"{celebratoryEmote}\"')
        elif outOfTimeEmote is not None and not isinstance(outOfTimeEmote, str):
            raise TypeError(f'outOfTimeEmote argument is malformed: \"{outOfTimeEmote}\"')
        elif wrongAnswerEmote is not None and not isinstance(wrongAnswerEmote, str):
            raise TypeError(f'wrongAnswerEmote argument is malformed: \"{wrongAnswerEmote}\"')
        elif not isinstance(cacheTimeBuffer, timedelta):
            raise TypeError(f'cacheTimeBuffer argument is malformed: \"{cacheTimeBuffer}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__celebratoryEmote: str | None = celebratoryEmote
        self.__outOfTimeEmote: str | None = outOfTimeEmote
        self.__wrongAnswerEmote: str | None = wrongAnswerEmote
        self.__cacheTimeBuffer: timedelta = cacheTimeBuffer

        self.__isAvailableCache: dict[TriviaTwitchEmoteType, bool | None] = dict()
        self.__timeCache: dict[TriviaTwitchEmoteType, datetime | None] =  dict()

    async def clearCaches(self):
        self.__isAvailableCache.clear()
        self.__timeCache.clear()
        self.__timber.log('TriviaTwitchEmoteHelper', 'Caches cleared')

    async def getCelebratoryEmote(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        celebratoryEmote = self.__celebratoryEmote
        if not utils.isValidStr(celebratoryEmote):
            return None

        charlesUserId = await self.__twitchFriendsUserIdRepository.getCharlesUserId()
        if not utils.isValidStr(charlesUserId):
            return None

        return await self.__getEmote(
            emoteText = celebratoryEmote,
            twitchChannelId = twitchChannelId,
            twitchEmoteChannelId = charlesUserId,
            emoteType = TriviaTwitchEmoteType.CELEBRATORY
        )

    async def __getEmote(
        self,
        emoteText: str,
        twitchChannelId: str,
        twitchEmoteChannelId: str,
        emoteType: TriviaTwitchEmoteType
    ) -> str | None:
        isAvailable = self.__isAvailableCache.get(emoteType, None)
        cachedTime = self.__timeCache.get(emoteType, None)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if cachedTime is not None and cachedTime + self.__cacheTimeBuffer >= now:
            if isAvailable is True:
                return emoteText
            else:
                return None

        twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(twitchChannelId)
        if not utils.isValidStr(twitchAccessToken):
            self.__isAvailableCache[emoteType] = False
            self.__cachedTime[emoteType] = now
            return None

        viableEmoteNames = await self.__twitchEmotesHelper.fetchViableSubscriptionEmoteNames(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchEmoteChannelId
        )

        emoteIsAvailable = emoteText in viableEmoteNames
        self.__isAvailableCache[emoteType] = emoteIsAvailable
        self.__timeCache[emoteType] = datetime.now(self.__timeZoneRepository.getDefault())

        if emoteIsAvailable:
            self.__timber.log('TriviaTwitchEmoteHelper', f'Emote is available ({emoteText=}) ({twitchChannelId=}) ({twitchEmoteChannelId=}) ({emoteType=})')
            return emoteText
        else:
            self.__timber.log('TriviaTwitchEmoteHelper', f'Emote isn\'t available ({emoteText=}) ({twitchChannelId=}) ({twitchEmoteChannelId=}) ({emoteType=})')
            return None

    async def getOutOfTimeEmote(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        outOfTimeEmote = self.__outOfTimeEmote
        if not utils.isValidStr(outOfTimeEmote):
            return None

        charlesUserId = await self.__twitchFriendsUserIdRepository.getCharlesUserId()
        if not utils.isValidStr(charlesUserId):
            return None

        return await self.__getEmote(
            emoteText = outOfTimeEmote,
            twitchChannelId = twitchChannelId,
            twitchEmoteChannelId = charlesUserId,
            emoteType = TriviaTwitchEmoteType.OUT_OF_TIME
        )

    async def getWrongAnswerEmote(self, twitchChannelId: str) -> str | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wrongAnswerEmote = self.__wrongAnswerEmote
        if not utils.isValidStr(wrongAnswerEmote):
            return None

        charlesUserId = await self.__twitchFriendsUserIdRepository.getCharlesUserId()
        if not utils.isValidStr(charlesUserId):
            return None

        return await self.__getEmote(
            emoteText = wrongAnswerEmote,
            twitchChannelId = twitchChannelId,
            twitchEmoteChannelId = charlesUserId,
            emoteType = TriviaTwitchEmoteType.WRONG_ANSWER
        )
