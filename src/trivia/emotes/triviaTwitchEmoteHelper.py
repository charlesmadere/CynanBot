from datetime import datetime, timedelta

from .triviaTwitchEmoteHelperInterface import TriviaTwitchChannelEmoteHelperInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from ...twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface


class TriviaTwitchEmoteHelper(TriviaTwitchChannelEmoteHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        cacheTimeDelta: timedelta = timedelta(hours = 3)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchEmotesHelper: TwitchEmotesHelperInterface = twitchEmotesHelper
        self.__twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = twitchFriendsUserIdRepository
        self.__cacheTimeDelta: timedelta = cacheTimeDelta

        self.__celebratoryCacheTime: datetime = datetime.now(timeZoneRepository.getDefault())
        self.__celebratoryEmote: str | None = None

    async def clearCaches(self):
        self.__celebratoryEmote = None
        self.__timber.log('TriviaTwitchEmoteHelper', 'Caches cleared')

    async def getCelebratoryEmote(self) -> str | None:
        charlesUserId = await self.__twitchFriendsUserIdRepository.getCharlesUserId()

        if not utils.isValidStr(charlesUserId):
            return None

        now = datetime.now(self.__timeZoneRepository.getDefault())
        celebratoryEmote = self.__celebratoryEmote

        if utils.isValidStr(celebratoryEmote) and self.__celebratoryCacheTime + self.__cacheTimeDelta >= now:
            return celebratoryEmote

        # TODO

        return None
